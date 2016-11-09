import java.util.Scanner;

public class Devoxx4kids {

    public static void main(String[] args) {
        Person p = new Person("Mr.", "Java", 10);
        p.introduce();
        Scanner sc = new Scanner(System.in);
        String line = null;
        while (line == null || line.length() > 0) {
            System.out.println("What do you want me to say? ");
            line = sc.nextLine();
            if (line.length() > 0) {
                p.say(line);
            }
        }
    }

}
