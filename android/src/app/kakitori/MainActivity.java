package app.kakitori;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.graphics.Color;
import android.graphics.Insets;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.LinearLayout;
import android.window.OnBackInvokedCallback;
import android.window.OnBackInvokedDispatcher;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;

public class MainActivity extends Activity {
    private static final int REQ_NOTIFY = 7;
    private WebView web;
    private LinearLayout root;
    private View topBar, bottomBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        boolean night = (getResources().getConfiguration().uiMode
                & Configuration.UI_MODE_NIGHT_MASK) == Configuration.UI_MODE_NIGHT_YES;

        web = new WebView(this);
        web.setBackgroundColor(night ? PAPER_DARK : PAPER_LIGHT);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(false);
        s.setAllowContentAccess(false);
        s.setUserAgentString(s.getUserAgentString() + " RenshuApp/1.8");
        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                // Links to other sites (like script.new) open in the phone's browser.
                Uri uri = request.getUrl();
                String scheme = uri.getScheme();
                if (("https".equals(scheme) || "http".equals(scheme))
                        && !"appassets.androidplatform.net".equals(uri.getHost())) {
                    try {
                        startActivity(new Intent(Intent.ACTION_VIEW, uri));
                    } catch (Exception ignored) { }
                }
                return true;
            }
        });
        web.addJavascriptInterface(new Bridge(), "KakitoriNative");
        setContentView(buildLayout());
        applyBars(night);
        listenForBack();
        Reminders.schedule(this); // re-arm in case the system cleared it
        web.loadDataWithBaseURL("https://appassets.androidplatform.net/renshu/",
                readAsset("index.html"), "text/html", "utf-8", null);
    }

    private static final int PAPER_LIGHT = 0xFFEDF0EE, SURFACE_LIGHT = 0xFFFAFBFA;
    private static final int PAPER_DARK = 0xFF10141B, SURFACE_DARK = 0xFF181E28;

    /**
     * The page fills the screen between two strips that sit under the status bar and the navigation bar.
     * From Android 15 apps always draw behind the system bars, so the strips take the bars' sizes
     * (and the keyboard's, when it is open) and carry the page's colors.
     */
    private View buildLayout() {
        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        topBar = new View(this);
        bottomBar = new View(this);
        root.addView(topBar, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0));
        root.addView(web, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));
        root.addView(bottomBar, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0));
        if (Build.VERSION.SDK_INT >= 30) {
            Window w = getWindow();
            w.setDecorFitsSystemWindows(false);
            w.setStatusBarColor(Color.TRANSPARENT);
            w.setNavigationBarColor(Color.TRANSPARENT);
            w.setNavigationBarContrastEnforced(false);
            w.setStatusBarContrastEnforced(false);
            root.setOnApplyWindowInsetsListener(new View.OnApplyWindowInsetsListener() {
                @Override
                public WindowInsets onApplyWindowInsets(View v, WindowInsets in) {
                    Insets bars = in.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                    Insets ime = in.getInsets(WindowInsets.Type.ime());
                    v.setPadding(bars.left, 0, bars.right, 0);
                    setHeight(topBar, bars.top);
                    setHeight(bottomBar, Math.max(bars.bottom, ime.bottom));
                    return WindowInsets.CONSUMED;
                }
            });
        }
        return root;
    }

    private static void setHeight(View v, int h) {
        ViewGroup.LayoutParams lp = v.getLayoutParams();
        if (lp.height != h) {
            lp.height = h;
            v.setLayoutParams(lp);
        }
    }

    /** Back first asks the page to close a panel or return to the Kana tab; otherwise the app goes to the background. */
    private void listenForBack() {
        if (Build.VERSION.SDK_INT >= 33) {
            getOnBackInvokedDispatcher().registerOnBackInvokedCallback(OnBackInvokedDispatcher.PRIORITY_DEFAULT,
                    new OnBackInvokedCallback() {
                        @Override
                        public void onBackInvoked() {
                            handleBack();
                        }
                    });
        }
    }

    private void handleBack() {
        if (web == null) {
            moveTaskToBack(true);
            return;
        }
        web.evaluateJavascript("(window.renshuBack && window.renshuBack()) ? '1' : '0'",
                new ValueCallback<String>() {
                    @Override
                    public void onReceiveValue(String value) {
                        if (!"\"1\"".equals(value)) moveTaskToBack(true);
                    }
                });
    }

    /** Calls the page makes into the app: theme bars and the daily reminder. */
    public class Bridge {
        @JavascriptInterface
        public String reminderState() {
            SharedPreferences p = Reminders.prefs(MainActivity.this);
            return "{\"on\":" + p.getBoolean("on", false)
                    + ",\"blocked\":" + !Reminders.canNotify(MainActivity.this)
                    + ",\"hour\":" + p.getInt("hour", 19)
                    + ",\"minute\":" + p.getInt("minute", 0) + "}";
        }

        /** Returns "scheduled", "off", "asking" (permission prompt shown) or "blocked". */
        @JavascriptInterface
        public String setReminder(boolean on, int hour, int minute) {
            Context c = MainActivity.this;
            SharedPreferences p = Reminders.prefs(c);
            p.edit().putInt("hour", Math.max(0, Math.min(23, hour))).putInt("minute", Math.max(0, Math.min(59, minute))).apply();
            if (!on) {
                p.edit().putBoolean("on", false).apply();
                Reminders.schedule(c);
                return "off";
            }
            if (Build.VERSION.SDK_INT >= 33 && c.checkSelfPermission(Reminders.POST) != PackageManager.PERMISSION_GRANTED) {
                boolean asked = p.getBoolean("asked", false);
                if (!asked || shouldShowRequestPermissionRationale(Reminders.POST)) {
                    p.edit().putBoolean("asked", true).apply();
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            requestPermissions(new String[]{Reminders.POST}, REQ_NOTIFY);
                        }
                    });
                    return "asking";
                }
                p.edit().putBoolean("on", false).apply();
                return "blocked";
            }
            if (!Reminders.canNotify(c)) {
                p.edit().putBoolean("on", false).apply();
                return "blocked";
            }
            p.edit().putBoolean("on", true).apply();
            Reminders.schedule(c);
            return "scheduled";
        }

        /** practiced: the day last practiced, as the page writes it. dueJson: review times in ms. */
        @JavascriptInterface
        public void setStudyState(String practiced, String dueJson) {
            Reminders.prefs(MainActivity.this).edit()
                    .putString("practiced", practiced == null ? "" : practiced)
                    .putString("due", dueJson == null ? "[]" : dueJson)
                    .apply();
        }

        @JavascriptInterface
        public String testReminder() {
            return Reminders.notifyNow(MainActivity.this, true) ? "sent" : "blocked";
        }

        /** The page sends the notification wording in the chosen language, so reminders match the app. */
        @JavascriptInterface
        public void setNotifyText(String title, String one, String many, String none, String channel) {
            Reminders.prefs(MainActivity.this).edit()
                    .putString("t_title", title).putString("t_one", one).putString("t_many", many)
                    .putString("t_none", none).putString("t_channel", channel).apply();
        }

        @JavascriptInterface
        public void openNotificationSettings() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    try {
                        startActivity(new Intent(Settings.ACTION_APP_NOTIFICATION_SETTINGS)
                                .putExtra(Settings.EXTRA_APP_PACKAGE, getPackageName()));
                    } catch (Exception ignored) { }
                }
            });
        }

        @JavascriptInterface
        public void setDark(final boolean dark) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    applyBars(dark);
                }
            });
        }
    }

    private void applyBars(boolean dark) {
        int paper = dark ? PAPER_DARK : PAPER_LIGHT;
        int surface = dark ? SURFACE_DARK : SURFACE_LIGHT;
        Window w = getWindow();
        if (root != null) {
            root.setBackgroundColor(paper);
            topBar.setBackgroundColor(paper);
            bottomBar.setBackgroundColor(surface);
        }
        if (web != null) web.setBackgroundColor(paper);
        if (Build.VERSION.SDK_INT >= 30) {
            WindowInsetsController c = w.getInsetsController();
            int light = WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS | WindowInsetsController.APPEARANCE_LIGHT_NAVIGATION_BARS;
            if (c != null) c.setSystemBarsAppearance(dark ? 0 : light, light);
        } else {
            w.setStatusBarColor(paper);
            w.setNavigationBarColor(surface);
            View d = w.getDecorView();
            int lightFlags = View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR;
            int flags = d.getSystemUiVisibility();
            d.setSystemUiVisibility(dark ? (flags & ~lightFlags) : (flags | lightFlags));
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode != REQ_NOTIFY) return;
        boolean ok = grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED && Reminders.canNotify(this);
        Reminders.prefs(this).edit().putBoolean("on", ok).apply();
        Reminders.schedule(this);
        if (web != null) {
            web.evaluateJavascript("window.kakitoriReminderResult && window.kakitoriReminderResult(" + ok + ")", null);
        }
    }

    /** Android 12 and older. Newer versions use the callback registered in listenForBack(). */
    @Override
    public void onBackPressed() {
        handleBack();
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (web != null) web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onDestroy() {
        if (web != null) {
            web.destroy();
            web = null;
        }
        super.onDestroy();
    }

    private String readAsset(String name) {
        InputStream in = null;
        try {
            in = getAssets().open(name);
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[65536];
            int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
            return out.toString("UTF-8");
        } catch (Exception e) {
            return "<p style='font:16px sans-serif;padding:24px'>Couldn't load the app files. Try reinstalling.</p>";
        } finally {
            if (in != null) {
                try { in.close(); } catch (Exception ignored) { }
            }
        }
    }
}
