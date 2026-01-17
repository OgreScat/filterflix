/**
 * FilterFlix Popup Script
 * Handles settings UI and communication with content script
 */

(function() {
  'use strict';

  // Default settings
  const defaults = {
    enabled: true,
    filterMode: 'skip',
    enabledTypes: ['nudity', 'profanity', 'violence'],
    minSeverity: 1
  };

  // DOM Elements
  const elements = {
    masterToggle: document.getElementById('masterToggle'),
    status: document.getElementById('status'),
    modeButtons: document.querySelectorAll('.mode-btn'),
    typeCheckboxes: document.querySelectorAll('.type-checkbox input'),
    severitySlider: document.getElementById('severitySlider'),
    severityValue: document.getElementById('severityValue')
  };

  // ═══════════════════════════════════════════════════════════════
  // SETTINGS MANAGEMENT
  // ═══════════════════════════════════════════════════════════════

  async function loadSettings() {
    try {
      const result = await chrome.storage.local.get(Object.keys(defaults));
      const settings = { ...defaults, ...result };

      // Master toggle
      elements.masterToggle.checked = settings.enabled;

      // Filter mode
      elements.modeButtons.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === settings.filterMode);
      });

      // Content types
      elements.typeCheckboxes.forEach(checkbox => {
        checkbox.checked = settings.enabledTypes.includes(checkbox.value);
      });

      // Severity
      elements.severitySlider.value = settings.minSeverity;
      updateSeverityDisplay(settings.minSeverity);

      updateStatus(settings);
    } catch (err) {
      console.error('Error loading settings:', err);
    }
  }

  async function saveSetting(key, value) {
    try {
      await chrome.storage.local.set({ [key]: value });
      console.log('Saved:', key, value);
    } catch (err) {
      console.error('Error saving setting:', err);
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // UI UPDATES
  // ═══════════════════════════════════════════════════════════════

  function updateStatus(settings) {
    const status = elements.status;

    if (!settings.enabled) {
      status.textContent = 'Filtering disabled';
      status.classList.remove('active');
      return;
    }

    const types = settings.enabledTypes;
    const mode = settings.filterMode;
    const modeText = mode === 'skip' ? 'skipping' : mode === 'mute' ? 'muting' : 'blurring';

    if (types.length === 0) {
      status.textContent = 'No content types selected';
      status.classList.remove('active');
    } else {
      status.textContent = `Actively ${modeText} ${types.length} content type${types.length > 1 ? 's' : ''}`;
      status.classList.add('active');
    }
  }

  function updateSeverityDisplay(value) {
    elements.severityValue.textContent = value + '+';
  }

  function getEnabledTypes() {
    return Array.from(elements.typeCheckboxes)
      .filter(cb => cb.checked)
      .map(cb => cb.value);
  }

  async function getCurrentSettings() {
    const result = await chrome.storage.local.get(Object.keys(defaults));
    return { ...defaults, ...result };
  }

  // ═══════════════════════════════════════════════════════════════
  // EVENT HANDLERS
  // ═══════════════════════════════════════════════════════════════

  // Master toggle
  elements.masterToggle.addEventListener('change', async () => {
    const enabled = elements.masterToggle.checked;
    await saveSetting('enabled', enabled);
    const settings = await getCurrentSettings();
    updateStatus(settings);
  });

  // Filter mode buttons
  elements.modeButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      elements.modeButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      await saveSetting('filterMode', btn.dataset.mode);
      const settings = await getCurrentSettings();
      updateStatus(settings);
    });
  });

  // Content type checkboxes
  elements.typeCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', async () => {
      const enabledTypes = getEnabledTypes();
      await saveSetting('enabledTypes', enabledTypes);
      const settings = await getCurrentSettings();
      updateStatus(settings);
    });
  });

  // Severity slider
  elements.severitySlider.addEventListener('input', () => {
    updateSeverityDisplay(elements.severitySlider.value);
  });

  elements.severitySlider.addEventListener('change', async () => {
    const value = parseInt(elements.severitySlider.value);
    await saveSetting('minSeverity', value);
  });

  // ═══════════════════════════════════════════════════════════════
  // INITIALIZATION
  // ═══════════════════════════════════════════════════════════════

  loadSettings();

})();
