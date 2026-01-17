/**
 * FilterFlix Timestamp Tools
 * Utilities for loading, parsing, and managing timestamp data
 */

// ═══════════════════════════════════════════════════════════════
// TIME PARSING & FORMATTING
// ═══════════════════════════════════════════════════════════════

/**
 * Convert HH:MM:SS string to seconds
 * @param {string} timeStr - Time in HH:MM:SS or MM:SS format
 * @returns {number} Time in seconds
 */
function parseTimestamp(timeStr) {
  if (typeof timeStr === 'number') return timeStr;

  const parts = timeStr.split(':').map(Number);

  if (parts.length === 3) {
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  } else if (parts.length === 2) {
    return parts[0] * 60 + parts[1];
  }

  return parseFloat(timeStr) || 0;
}

/**
 * Convert seconds to HH:MM:SS string
 * @param {number} seconds - Time in seconds
 * @returns {string} Formatted time string
 */
function formatTimestamp(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);

  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

// ═══════════════════════════════════════════════════════════════
// TIMESTAMP LOADING
// ═══════════════════════════════════════════════════════════════

/**
 * Load timestamps from chrome.storage.local
 * @param {string} imdbId - IMDb ID of the movie
 * @returns {Promise<Object|null>} Timestamp data or null
 */
async function loadTimestamps(imdbId) {
  try {
    const key = `timestamps_${imdbId}`;
    const result = await chrome.storage.local.get(key);

    if (result[key]) {
      return result[key];
    }

    // Try loading from bundled sample data
    const sampleKey = `sample_${imdbId}`;
    const sampleResult = await chrome.storage.local.get(sampleKey);

    return sampleResult[sampleKey] || null;
  } catch (err) {
    console.error('[FilterFlix] Error loading timestamps:', err);
    return null;
  }
}

/**
 * Save timestamps to chrome.storage.local
 * @param {string} imdbId - IMDb ID
 * @param {Object} data - Timestamp data object
 */
async function saveTimestamps(imdbId, data) {
  try {
    const key = `timestamps_${imdbId}`;
    await chrome.storage.local.set({ [key]: data });
    console.log('[FilterFlix] Saved timestamps for:', imdbId);
  } catch (err) {
    console.error('[FilterFlix] Error saving timestamps:', err);
  }
}

/**
 * Load timestamps from remote URL
 * @param {string} url - URL to fetch timestamps from
 * @returns {Promise<Object|null>} Timestamp data or null
 */
async function loadTimestampsFromUrl(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
  } catch (err) {
    console.error('[FilterFlix] Error fetching timestamps:', err);
    return null;
  }
}

// ═══════════════════════════════════════════════════════════════
// TIMESTAMP MATCHING
// ═══════════════════════════════════════════════════════════════

/**
 * Find active segment at current playback time
 * @param {number} currentTime - Current video time in seconds
 * @param {Array} timestamps - Array of timestamp segments
 * @param {Object} filters - Filter settings {types: [], minSeverity: number}
 * @returns {Object|null} Active segment or null
 */
function matchCurrentTime(currentTime, timestamps, filters = {}) {
  const { types = ['nudity', 'profanity', 'violence'], minSeverity = 1 } = filters;

  for (const segment of timestamps) {
    // Check if type is enabled
    if (!types.includes(segment.type)) continue;

    // Check severity threshold
    if (segment.severity < minSeverity) continue;

    const start = parseTimestamp(segment.start);
    const end = parseTimestamp(segment.end);

    if (currentTime >= start && currentTime < end) {
      return {
        segment,
        start,
        end,
        remaining: end - currentTime
      };
    }
  }

  return null;
}

/**
 * Get all upcoming segments within a time window
 * @param {number} currentTime - Current time in seconds
 * @param {Array} timestamps - Array of timestamp segments
 * @param {number} windowSeconds - Look-ahead window in seconds
 * @returns {Array} Upcoming segments
 */
function getUpcomingSegments(currentTime, timestamps, windowSeconds = 60) {
  return timestamps
    .map(segment => ({
      ...segment,
      startSeconds: parseTimestamp(segment.start),
      endSeconds: parseTimestamp(segment.end)
    }))
    .filter(segment => {
      return segment.startSeconds > currentTime &&
             segment.startSeconds <= currentTime + windowSeconds;
    })
    .sort((a, b) => a.startSeconds - b.startSeconds);
}

// ═══════════════════════════════════════════════════════════════
// VALIDATION
// ═══════════════════════════════════════════════════════════════

/**
 * Validate a timestamp object against schema requirements
 * @param {Object} timestamp - Single timestamp object
 * @returns {Object} {valid: boolean, errors: string[]}
 */
function validateTimestamp(timestamp) {
  const errors = [];
  const validTypes = ['nudity', 'profanity', 'violence', 'substances', 'frightening'];
  const timePattern = /^[0-9]{2}:[0-9]{2}:[0-9]{2}$/;

  // Required fields
  if (!timestamp.start) errors.push('Missing start time');
  if (!timestamp.end) errors.push('Missing end time');
  if (!timestamp.type) errors.push('Missing type');
  if (timestamp.severity === undefined) errors.push('Missing severity');

  // Format validation
  if (timestamp.start && !timePattern.test(timestamp.start)) {
    errors.push('Invalid start time format (expected HH:MM:SS)');
  }
  if (timestamp.end && !timePattern.test(timestamp.end)) {
    errors.push('Invalid end time format (expected HH:MM:SS)');
  }

  // Type validation
  if (timestamp.type && !validTypes.includes(timestamp.type)) {
    errors.push(`Invalid type: ${timestamp.type}. Must be one of: ${validTypes.join(', ')}`);
  }

  // Severity validation
  if (timestamp.severity !== undefined) {
    if (!Number.isInteger(timestamp.severity) ||
        timestamp.severity < 1 ||
        timestamp.severity > 10) {
      errors.push('Severity must be integer between 1-10');
    }
  }

  // Logical validation
  if (timestamp.start && timestamp.end) {
    const startSec = parseTimestamp(timestamp.start);
    const endSec = parseTimestamp(timestamp.end);
    if (endSec <= startSec) {
      errors.push('End time must be after start time');
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Validate entire timestamp file
 * @param {Object} data - Full timestamp data object
 * @returns {Object} {valid: boolean, errors: string[]}
 */
function validateTimestampFile(data) {
  const errors = [];
  const imdbPattern = /^tt[0-9]+$/;

  // Required fields
  if (!data.title) errors.push('Missing title');
  if (!data.imdb_id) errors.push('Missing imdb_id');
  if (!data.timestamps || !Array.isArray(data.timestamps)) {
    errors.push('Missing or invalid timestamps array');
  }

  // IMDb ID format
  if (data.imdb_id && !imdbPattern.test(data.imdb_id)) {
    errors.push('Invalid imdb_id format (expected tt followed by numbers)');
  }

  // Validate each timestamp
  if (data.timestamps && Array.isArray(data.timestamps)) {
    data.timestamps.forEach((ts, index) => {
      const result = validateTimestamp(ts);
      if (!result.valid) {
        errors.push(`Timestamp ${index}: ${result.errors.join(', ')}`);
      }
    });
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

// ═══════════════════════════════════════════════════════════════
// STATISTICS
// ═══════════════════════════════════════════════════════════════

/**
 * Get statistics for a timestamp file
 * @param {Object} data - Timestamp data object
 * @returns {Object} Statistics summary
 */
function getTimestampStats(data) {
  if (!data.timestamps || !Array.isArray(data.timestamps)) {
    return null;
  }

  const stats = {
    total: data.timestamps.length,
    byType: {},
    bySeverity: { low: 0, medium: 0, high: 0 },
    totalFilterTime: 0,
    verified: 0,
    unverified: 0
  };

  data.timestamps.forEach(ts => {
    // Count by type
    stats.byType[ts.type] = (stats.byType[ts.type] || 0) + 1;

    // Count by severity
    if (ts.severity <= 3) stats.bySeverity.low++;
    else if (ts.severity <= 6) stats.bySeverity.medium++;
    else stats.bySeverity.high++;

    // Calculate total filter time
    const duration = parseTimestamp(ts.end) - parseTimestamp(ts.start);
    stats.totalFilterTime += duration;

    // Count verified
    if (ts.verified) stats.verified++;
    else stats.unverified++;
  });

  stats.totalFilterTimeFormatted = formatTimestamp(stats.totalFilterTime);

  return stats;
}

// ═══════════════════════════════════════════════════════════════
// EXPORTS (for Node.js usage)
// ═══════════════════════════════════════════════════════════════

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    parseTimestamp,
    formatTimestamp,
    loadTimestamps,
    saveTimestamps,
    loadTimestampsFromUrl,
    matchCurrentTime,
    getUpcomingSegments,
    validateTimestamp,
    validateTimestampFile,
    getTimestampStats
  };
}
