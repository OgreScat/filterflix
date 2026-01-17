/**
 * FilterFlix Content Script
 * Detects video elements on streaming platforms and applies content filtering
 */

(function() {
  'use strict';

  // ═══════════════════════════════════════════════════════════════
  // CONFIGURATION
  // ═══════════════════════════════════════════════════════════════

  const CONFIG = {
    POLL_INTERVAL: 500,
    CHECK_INTERVAL: 100,
    ADVANCEMENT_BUFFER: 0.5,
    BLUR_AMOUNT: '30px',
    DEBUG: true
  };

  // Platform detection patterns
  const PLATFORMS = {
    netflix: {
      pattern: /netflix\.com/,
      videoSelector: 'video',
      titleSelector: '[data-uia="video-title"]'
    },
    prime: {
      pattern: /primevideo\.com|amazon\.com\/gp\/video/,
      videoSelector: 'video',
      titleSelector: '.atvwebplayersdk-title-text'
    },
    disney: {
      pattern: /disneyplus\.com/,
      videoSelector: 'video',
      titleSelector: '[data-testid="title-field"]'
    },
    hbo: {
      pattern: /max\.com|hbomax\.com/,
      videoSelector: 'video',
      titleSelector: '[class*="Title"]'
    },
    hulu: {
      pattern: /hulu\.com/,
      videoSelector: 'video',
      titleSelector: '[class*="title"]'
    }
  };

  // ═══════════════════════════════════════════════════════════════
  // STATE MANAGEMENT
  // ═══════════════════════════════════════════════════════════════

  const state = {
    enabled: true,
    filterMode: 'skip', // skip, mute, blur
    enabledTypes: ['nudity', 'profanity', 'violence'],
    minSeverity: 1,
    currentPlatform: null,
    videoElement: null,
    timestamps: [],
    currentMovieId: null,
    isFiltering: false,
    originalMuted: false,
    blurOverlay: null,
    badge: null,
    checkInterval: null
  };

  // ═══════════════════════════════════════════════════════════════
  // UTILITY FUNCTIONS
  // ═══════════════════════════════════════════════════════════════

  function log(...args) {
    if (CONFIG.DEBUG) {
      console.log('[FilterFlix]', ...args);
    }
  }

  function parseTimestamp(timeStr) {
    const parts = timeStr.split(':').map(Number);
    if (parts.length === 3) {
      return parts[0] * 3600 + parts[1] * 60 + parts[2];
    } else if (parts.length === 2) {
      return parts[0] * 60 + parts[1];
    }
    return parseFloat(timeStr) || 0;
  }

  function formatTimestamp(seconds) {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  }

  // ═══════════════════════════════════════════════════════════════
  // PLATFORM DETECTION
  // ═══════════════════════════════════════════════════════════════

  function detectPlatform() {
    const url = window.location.href;
    for (const [name, config] of Object.entries(PLATFORMS)) {
      if (config.pattern.test(url)) {
        log('Detected platform:', name);
        return { name, config };
      }
    }
    return null;
  }

  // ═══════════════════════════════════════════════════════════════
  // VIDEO DETECTION
  // ═══════════════════════════════════════════════════════════════

  function findVideoElement() {
    if (!state.currentPlatform) return null;

    const selector = state.currentPlatform.config.videoSelector;
    const videos = document.querySelectorAll(selector);

    // Find the largest video (likely the main content)
    let mainVideo = null;
    let maxArea = 0;

    videos.forEach(video => {
      const rect = video.getBoundingClientRect();
      const area = rect.width * rect.height;
      if (area > maxArea && area > 10000) { // Min 100x100
        maxArea = area;
        mainVideo = video;
      }
    });

    return mainVideo;
  }

  // ═══════════════════════════════════════════════════════════════
  // TIMESTAMP MANAGEMENT
  // ═══════════════════════════════════════════════════════════════

  async function loadTimestamps() {
    try {
      const result = await chrome.storage.local.get(['timestamps', 'currentMovieId']);

      if (result.timestamps && result.currentMovieId) {
        state.timestamps = result.timestamps;
        state.currentMovieId = result.currentMovieId;
        log('Loaded timestamps for:', result.currentMovieId, state.timestamps.length, 'segments');
      } else {
        // Load demo timestamps for testing
        state.timestamps = getDemoTimestamps();
        log('Using demo timestamps');
      }
    } catch (err) {
      log('Error loading timestamps:', err);
      state.timestamps = getDemoTimestamps();
    }
  }

  function getDemoTimestamps() {
    // Demo timestamps for testing - will trigger at common intervals
    return [
      {
        start: '00:00:30',
        end: '00:00:35',
        type: 'profanity',
        severity: 5,
        description: 'Test segment - mild profanity'
      },
      {
        start: '00:02:00',
        end: '00:02:10',
        type: 'violence',
        severity: 7,
        description: 'Test segment - action violence'
      },
      {
        start: '00:05:00',
        end: '00:05:15',
        type: 'nudity',
        severity: 8,
        description: 'Test segment - nudity'
      }
    ];
  }

  function findActiveSegment(currentTime) {
    for (const segment of state.timestamps) {
      const start = parseTimestamp(segment.start);
      const end = parseTimestamp(segment.end);

      // Check if this segment type is enabled
      if (!state.enabledTypes.includes(segment.type)) continue;

      // Check severity threshold
      if (segment.severity < state.minSeverity) continue;

      // Check if we're in this segment
      if (currentTime >= start && currentTime < end) {
        return { segment, start, end };
      }
    }
    return null;
  }

  // ═══════════════════════════════════════════════════════════════
  // FILTER ACTIONS
  // ═══════════════════════════════════════════════════════════════

  function applySkip(video, endTime) {
    log('SKIP: Jumping to', formatTimestamp(endTime + CONFIG.ADVANCEMENT_BUFFER));
    video.currentTime = endTime + CONFIG.ADVANCEMENT_BUFFER;
    showNotification('Skipped filtered content');
  }

  function applyMute(video, segment) {
    if (!state.isFiltering) {
      state.originalMuted = video.muted;
      video.muted = true;
      state.isFiltering = true;
      log('MUTE: Audio muted for segment');
      showNotification('Audio muted - filtered content');
    }
  }

  function restoreMute(video) {
    if (state.isFiltering && state.filterMode === 'mute') {
      video.muted = state.originalMuted;
      state.isFiltering = false;
      log('MUTE: Audio restored');
    }
  }

  function applyBlur(video) {
    if (!state.blurOverlay) {
      createBlurOverlay(video);
    }
    state.blurOverlay.style.display = 'block';
    state.isFiltering = true;
    log('BLUR: Video blurred');
    showNotification('Video blurred - filtered content');
  }

  function removeBlur() {
    if (state.blurOverlay) {
      state.blurOverlay.style.display = 'none';
    }
    state.isFiltering = false;
    log('BLUR: Blur removed');
  }

  function createBlurOverlay(video) {
    const overlay = document.createElement('div');
    overlay.id = 'filterflix-blur-overlay';
    overlay.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      backdrop-filter: blur(${CONFIG.BLUR_AMOUNT});
      -webkit-backdrop-filter: blur(${CONFIG.BLUR_AMOUNT});
      background: rgba(0, 0, 0, 0.3);
      display: none;
      z-index: 9998;
      pointer-events: none;
    `;

    // Position relative to video
    const parent = video.parentElement;
    if (parent) {
      parent.style.position = 'relative';
      parent.appendChild(overlay);
    }

    state.blurOverlay = overlay;
  }

  // ═══════════════════════════════════════════════════════════════
  // UI COMPONENTS
  // ═══════════════════════════════════════════════════════════════

  function createBadge() {
    if (state.badge) return;

    const badge = document.createElement('div');
    badge.id = 'filterflix-badge';
    badge.innerHTML = `
      <div class="ff-badge-inner">
        <span class="ff-icon">FF</span>
        <span class="ff-status">${state.enabled ? 'ON' : 'OFF'}</span>
      </div>
    `;
    badge.style.cssText = `
      position: fixed;
      bottom: 80px;
      right: 20px;
      width: 50px;
      height: 50px;
      background: ${state.enabled ? 'linear-gradient(135deg, #6366f1, #8b5cf6)' : '#6b7280'};
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 10000;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      transition: all 0.2s ease;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    `;

    const inner = badge.querySelector('.ff-badge-inner');
    inner.style.cssText = `
      display: flex;
      flex-direction: column;
      align-items: center;
      color: white;
      font-size: 10px;
      font-weight: 600;
    `;

    const icon = badge.querySelector('.ff-icon');
    icon.style.cssText = `
      font-size: 14px;
      font-weight: 700;
    `;

    badge.addEventListener('click', toggleEnabled);
    badge.addEventListener('mouseenter', () => {
      badge.style.transform = 'scale(1.1)';
    });
    badge.addEventListener('mouseleave', () => {
      badge.style.transform = 'scale(1)';
    });

    document.body.appendChild(badge);
    state.badge = badge;
    log('Badge created');
  }

  function updateBadge() {
    if (!state.badge) return;

    state.badge.style.background = state.enabled
      ? 'linear-gradient(135deg, #6366f1, #8b5cf6)'
      : '#6b7280';

    const status = state.badge.querySelector('.ff-status');
    if (status) {
      status.textContent = state.enabled ? 'ON' : 'OFF';
    }
  }

  function showNotification(message) {
    const existing = document.getElementById('filterflix-notification');
    if (existing) existing.remove();

    const notification = document.createElement('div');
    notification.id = 'filterflix-notification';
    notification.textContent = message;
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: white;
      padding: 12px 20px;
      border-radius: 8px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      font-weight: 500;
      z-index: 10001;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      animation: ffSlideIn 0.3s ease;
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.style.animation = 'ffSlideOut 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }

  // ═══════════════════════════════════════════════════════════════
  // MAIN FILTERING LOGIC
  // ═══════════════════════════════════════════════════════════════

  function checkVideoTime() {
    if (!state.enabled || !state.videoElement) return;

    const video = state.videoElement;
    const currentTime = video.currentTime;
    const active = findActiveSegment(currentTime);

    if (active) {
      const { segment, end } = active;

      switch (state.filterMode) {
        case 'skip':
          applySkip(video, end);
          break;
        case 'mute':
          applyMute(video, segment);
          break;
        case 'blur':
          applyBlur(video);
          break;
      }
    } else {
      // No active segment - restore normal state
      if (state.isFiltering) {
        if (state.filterMode === 'mute') {
          restoreMute(video);
        } else if (state.filterMode === 'blur') {
          removeBlur();
        }
        state.isFiltering = false;
      }
    }
  }

  function startMonitoring(video) {
    if (state.checkInterval) {
      clearInterval(state.checkInterval);
    }

    state.videoElement = video;
    state.checkInterval = setInterval(checkVideoTime, CONFIG.CHECK_INTERVAL);

    // Also listen for video events
    video.addEventListener('timeupdate', checkVideoTime);
    video.addEventListener('seeked', checkVideoTime);

    log('Started monitoring video');
  }

  function stopMonitoring() {
    if (state.checkInterval) {
      clearInterval(state.checkInterval);
      state.checkInterval = null;
    }

    if (state.videoElement) {
      state.videoElement.removeEventListener('timeupdate', checkVideoTime);
      state.videoElement.removeEventListener('seeked', checkVideoTime);
    }

    state.videoElement = null;
    log('Stopped monitoring');
  }

  // ═══════════════════════════════════════════════════════════════
  // SETTINGS & COMMUNICATION
  // ═══════════════════════════════════════════════════════════════

  async function loadSettings() {
    try {
      const result = await chrome.storage.local.get([
        'enabled',
        'filterMode',
        'enabledTypes',
        'minSeverity'
      ]);

      if (result.enabled !== undefined) state.enabled = result.enabled;
      if (result.filterMode) state.filterMode = result.filterMode;
      if (result.enabledTypes) state.enabledTypes = result.enabledTypes;
      if (result.minSeverity !== undefined) state.minSeverity = result.minSeverity;

      log('Settings loaded:', {
        enabled: state.enabled,
        filterMode: state.filterMode,
        enabledTypes: state.enabledTypes,
        minSeverity: state.minSeverity
      });
    } catch (err) {
      log('Error loading settings:', err);
    }
  }

  function toggleEnabled() {
    state.enabled = !state.enabled;
    chrome.storage.local.set({ enabled: state.enabled });
    updateBadge();

    if (!state.enabled) {
      // Clean up any active filtering
      if (state.isFiltering) {
        if (state.filterMode === 'mute' && state.videoElement) {
          restoreMute(state.videoElement);
        } else if (state.filterMode === 'blur') {
          removeBlur();
        }
        state.isFiltering = false;
      }
    }

    showNotification(`FilterFlix ${state.enabled ? 'enabled' : 'disabled'}`);
    log('Toggled enabled:', state.enabled);
  }

  // Listen for settings changes from popup
  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'local') return;

    if (changes.enabled) state.enabled = changes.enabled.newValue;
    if (changes.filterMode) state.filterMode = changes.filterMode.newValue;
    if (changes.enabledTypes) state.enabledTypes = changes.enabledTypes.newValue;
    if (changes.minSeverity) state.minSeverity = changes.minSeverity.newValue;
    if (changes.timestamps) {
      state.timestamps = changes.timestamps.newValue;
      log('Timestamps updated:', state.timestamps.length, 'segments');
    }

    updateBadge();
    log('Settings updated from storage');
  });

  // ═══════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════════════════════════════

  let pollInterval = null;

  function pollForVideo() {
    const video = findVideoElement();

    if (video && video !== state.videoElement) {
      log('Video element found');
      startMonitoring(video);
    } else if (!video && state.videoElement) {
      log('Video element lost');
      stopMonitoring();
    }
  }

  async function init() {
    log('Initializing FilterFlix...');

    // Detect platform
    state.currentPlatform = detectPlatform();
    if (!state.currentPlatform) {
      log('Not a supported streaming platform');
      return;
    }

    log('Platform:', state.currentPlatform.name);

    // Load settings and timestamps
    await loadSettings();
    await loadTimestamps();

    // Create UI
    createBadge();

    // Start polling for video
    pollInterval = setInterval(pollForVideo, CONFIG.POLL_INTERVAL);
    pollForVideo(); // Initial check

    log('FilterFlix initialized successfully');
  }

  // Inject CSS animations
  const style = document.createElement('style');
  style.textContent = `
    @keyframes ffSlideIn {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes ffSlideOut {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(100%); opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // Start when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
