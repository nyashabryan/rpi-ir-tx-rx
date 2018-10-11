import org.jfugue.player.Player;
import org.jfugue.realtime.RealtimePlayer;
import org.jfugue.pattern.Pattern;

public class test {
  public static void main(String[] args) {
    Player player = new Player();

    Pattern pattern = new Pattern("X[Volume]=" + args[2] +" " + args[0]+args[1]);
    player.play(pattern);

  }
}