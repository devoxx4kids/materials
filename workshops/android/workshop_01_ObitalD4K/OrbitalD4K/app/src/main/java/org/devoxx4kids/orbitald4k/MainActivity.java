package org.devoxx4kids.orbitald4k;

import android.graphics.drawable.Animatable;
import android.graphics.drawable.Drawable;
import android.support.graphics.drawable.AnimatedVectorDrawableCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.TextView;

import java.util.concurrent.TimeUnit;

public class MainActivity extends AppCompatActivity {

    private static final double RADIUS = 6_378.14;
    private static final double GRAVITY = 6.67 * Math.pow(10, -11);
    private static final double EARTH_MASS = 5.9736 * Math.pow(10, 24);

    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        AnimatedVectorDrawableCompat myDrawable = AnimatedVectorDrawableCompat.create(this, R.drawable.orbital_animated_vector);
        imageView = (ImageView) findViewById(R.id.drawable);
        imageView.setImageDrawable(myDrawable);
    }

    public void calculate(View view) {
        EditText editView = (EditText)findViewById(R.id.editText);
        Integer distance = Integer.valueOf(editView.getText().toString());

        double period = Math.sqrt(4 * Math.pow(Math.PI, 2) * Math.pow((distance + RADIUS) * 1000, 3) / (GRAVITY * EARTH_MASS));

        TextView resultView = (TextView) findViewById(R.id.textView);
        String hms = String.format("%02dh %02dm %02ds", TimeUnit.SECONDS.toHours((long) period),
                TimeUnit.SECONDS.toMinutes((long) period) % 60, (long) period % 60);
        resultView.setText(hms);


        Drawable drawable = imageView.getDrawable();
        if (drawable instanceof Animatable) {
            if (!((Animatable) drawable).isRunning())
                ((Animatable) drawable).start();
        }
    }
}
