package app.renshu;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/** Fires the daily reminder, and re-arms it after a restart, an app update or a clock change. */
public class ReminderReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context c, Intent intent) {
        String action = intent != null ? intent.getAction() : null;
        if (Reminders.ACTION_REMIND.equals(action)) Reminders.notifyNow(c, false);
        Reminders.schedule(c);
    }
}
