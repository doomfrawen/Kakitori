package app.renshu;

import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;
import org.json.JSONArray;
import java.util.Calendar;

/** The daily practice reminder: scheduling, and the notification itself. */
final class Reminders {
    static final String ACTION_REMIND = "app.renshu.action.REMIND";
    static final String POST = "android.permission.POST_NOTIFICATIONS";
    private static final String CHANNEL = "practice";

    private Reminders() { }

    static SharedPreferences prefs(Context c) {
        return c.getSharedPreferences("reminders", Context.MODE_PRIVATE);
    }

    /** True when the app is allowed to show notifications right now. */
    static boolean canNotify(Context c) {
        if (Build.VERSION.SDK_INT >= 33 && c.checkSelfPermission(POST) != PackageManager.PERMISSION_GRANTED) {
            return false;
        }
        NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
        return nm != null && nm.areNotificationsEnabled();
    }

    private static PendingIntent alarmIntent(Context c) {
        Intent i = new Intent(c, ReminderReceiver.class).setAction(ACTION_REMIND);
        return PendingIntent.getBroadcast(c, 0, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    /** Arms the next reminder, or cancels it when reminders are off. Safe to call any time. */
    static void schedule(Context c) {
        AlarmManager am = (AlarmManager) c.getSystemService(Context.ALARM_SERVICE);
        if (am == null) return;
        PendingIntent pi = alarmIntent(c);
        am.cancel(pi);
        SharedPreferences p = prefs(c);
        if (!p.getBoolean("on", false)) return;
        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, p.getInt("hour", 19));
        cal.set(Calendar.MINUTE, p.getInt("minute", 0));
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        if (cal.getTimeInMillis() <= System.currentTimeMillis() + 5000) cal.add(Calendar.DAY_OF_YEAR, 1);
        // Inexact but allowed during Doze, and needs no special alarm permission.
        am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, cal.getTimeInMillis(), pi);
    }

    /** Today's date in the same form the page uses: year-month-day without zero padding. */
    static String today() {
        Calendar cal = Calendar.getInstance();
        return cal.get(Calendar.YEAR) + "-" + (cal.get(Calendar.MONTH) + 1) + "-" + cal.get(Calendar.DAY_OF_MONTH);
    }

    private static int dueCount(Context c) {
        try {
            JSONArray a = new JSONArray(prefs(c).getString("due", "[]"));
            double now = System.currentTimeMillis();
            int n = 0;
            for (int k = 0; k < a.length(); k++) {
                if (a.optDouble(k, Double.MAX_VALUE) <= now) n++;
            }
            return n;
        } catch (Exception e) {
            return 0;
        }
    }

    /** Wording saved by the page in the user's language, or English until the app has been opened once. */
    private static String text(SharedPreferences p, String key, String fallback) {
        String s = p.getString(key, null);
        return s == null || s.isEmpty() ? fallback : s;
    }

    /**
     * Shows the reminder. Skipped on days already practiced, unless force is true (the test button).
     * Returns false only when notifications are blocked.
     */
    static boolean notifyNow(Context c, boolean force) {
        if (!canNotify(c)) return false;
        if (!force && today().equals(prefs(c).getString("practiced", ""))) return true;
        NotificationManager nm = (NotificationManager) c.getSystemService(Context.NOTIFICATION_SERVICE);
        SharedPreferences p = prefs(c);
        NotificationChannel ch = new NotificationChannel(CHANNEL, text(p, "t_channel", "Practice reminders"), NotificationManager.IMPORTANCE_DEFAULT);
        nm.createNotificationChannel(ch);

        int due = dueCount(c);
        String body = due == 1 ? text(p, "t_one", "1 review is ready. A few minutes keeps it fresh.")
                : due > 1 ? text(p, "t_many", "{n} reviews are ready. A few minutes keeps them fresh.").replace("{n}", String.valueOf(due))
                : text(p, "t_none", "A few minutes of writing keeps your kana fresh.");

        Intent open = c.getPackageManager().getLaunchIntentForPackage(c.getPackageName());
        if (open == null) open = new Intent(c, MainActivity.class);
        open.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_RESET_TASK_IF_NEEDED);
        PendingIntent pi = PendingIntent.getActivity(c, 1, open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);

        int icon = c.getResources().getIdentifier("ic_notify", "drawable", c.getPackageName());
        Notification n = new Notification.Builder(c, CHANNEL)
                .setSmallIcon(icon != 0 ? icon : android.R.drawable.ic_popup_reminder)
                .setContentTitle(text(p, "t_title", "Time to practice"))
                .setContentText(body)
                .setStyle(new Notification.BigTextStyle().bigText(body))
                .setColor(0xFF2B4878)
                .setAutoCancel(true)
                .setContentIntent(pi)
                .build();
        nm.notify(1, n);
        return true;
    }
}
