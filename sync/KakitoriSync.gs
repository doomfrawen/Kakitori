// Kakitori sync. Keeps your Kakitori progress in your own Google account.
// Paste this into a new Apps Script project (script.new), then
// Deploy > New deployment > Web app, Execute as: Me, Who has access: Anyone.
// Paste the Web app URL (ending in /exec) into Kakitori > Settings > Google sync.

var CHUNK = 8000; // Script properties hold up to 9 KB per value.

function doGet(e) {
  return handle_(null);
}

function doPost(e) {
  return handle_(e && e.postData ? e.postData.contents : '');
}

function handle_(body) {
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var props = PropertiesService.getScriptProperties();
    var all = props.getProperties();
    var oldCount = Number(all.n || 0);

    if (body) {
      var msg = JSON.parse(body);
      var data = String(msg.data || '');
      if (!data) return json_({ ok: false, error: 'empty' });
      var count = Math.ceil(data.length / CHUNK);
      var update = { n: String(count), t: String(Number(msg.t) || Date.now()) };
      for (var i = 0; i < count; i++) update['c' + i] = data.substr(i * CHUNK, CHUNK);
      props.setProperties(update);
      for (var j = count; j < oldCount; j++) props.deleteProperty('c' + j);
      return json_({ ok: true, t: Number(update.t) });
    }

    var parts = [];
    for (var k = 0; k < oldCount; k++) parts.push(all['c' + k] || '');
    return json_({ ok: true, t: Number(all.t || 0), data: parts.join('') });
  } catch (err) {
    return json_({ ok: false, error: String(err && err.message || err) });
  } finally {
    lock.releaseLock();
  }
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
