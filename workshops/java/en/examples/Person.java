public class Person {
    String firstName;
    String lastName;
    int age;

    // Constructor
    public Person(String firstName, String lastName, int age) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
    }

    public void introduce() {
        say(getIntroduction());
    }

    public void say(String statement) {
        System.out.println(statement);
    }

    private String getIntroduction() {
        String intro = "Hi! My name is " + firstName + " " + lastName + ". I am " + age + " years old. I think Java is fun! :)";
        return intro;
    }

}

