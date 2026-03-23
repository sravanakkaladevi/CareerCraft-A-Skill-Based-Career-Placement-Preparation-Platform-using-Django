from django.core.management.base import BaseCommand

from learn.models import Language, Lesson, Topic


JAVA_CONTENT = [
    {
        "topic": "Basics of Java",
        "summary": "Start with Java fundamentals, platform basics, language history, and the core concepts every beginner should know first.",
        "level": "beginner",
        "order": 1,
        "lessons": [
            {
                "title": "What is Java",
                "order": 1,
                "theory": """Java is a high-level, class-based, object-oriented programming language designed to be simple, secure, portable, and reliable.

It was created to help developers write code once and run it on many different systems without major changes. This idea is commonly described as "Write Once, Run Anywhere" because Java programs run on the Java Virtual Machine (JVM) instead of depending directly on one operating system.

Java is widely used in web applications, enterprise software, Android development, banking systems, cloud services, and backend platforms. It is popular in education and interviews because it teaches strong programming fundamentals such as classes, objects, inheritance, exception handling, and memory management.

Java source code is written in files with the .java extension. The compiler converts that code into bytecode, and the JVM executes the bytecode on the target machine.

In simple words, Java is a practical and industry-friendly programming language used to build everything from beginner programs to large-scale business applications.""",
                "syntax_example": """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, Java!");
    }
}""",
                "practice_note": "Write a simple Java program that prints your name, college, and favorite programming language.",
            },
            {
                "title": "History of Java",
                "order": 2,
                "theory": """Java was developed by James Gosling and his team at Sun Microsystems in the early 1990s. The project was initially created for consumer electronic devices and was first called Oak.

Later, Oak was renamed Java because the name Oak was already in use. Java was officially introduced in 1995 and quickly became popular because of its portability, security model, and support for internet-based applications.

During the growth of the web, Java applets were one of the early reasons for Java's fame. Over time, Java moved beyond applets and became a major language for enterprise software, backend systems, mobile applications, and large business platforms.

Sun Microsystems was later acquired by Oracle Corporation in 2010, and Oracle continues to maintain and evolve Java. Since then, Java has continued to receive updates, performance improvements, and new language features.

The history of Java shows how a language built for portability and reliability became one of the most important technologies in software development.""",
                "practice_note": "Prepare a short note on why Java became popular in both education and enterprise software.",
            },
            {
                "title": "Features of Java",
                "order": 3,
                "theory": """Java offers a set of features that make it one of the most trusted programming languages in the industry.

1. Object-Oriented: Java is based on classes and objects, which helps in building modular and reusable applications.
2. Platform Independent: Java code is compiled into bytecode, which can run on any system with a JVM.
3. Simple: Java removes many complex features from older languages and provides a clean, structured syntax.
4. Secure: Java has a strong runtime environment, bytecode verification, and controlled memory access.
5. Robust: Java supports exception handling, type checking, and automatic memory management through garbage collection.
6. Multithreaded: Java allows multiple tasks to run at the same time within one program.
7. Distributed: Java supports networking and distributed application development.
8. High Performance: While not as low-level as C or C++, Java provides strong performance through optimized runtime execution.

These features make Java a good choice for both beginners and professionals working on scalable software systems.""",
                "practice_note": "List five Java features and explain each one in one line using your own words.",
            },
            {
                "title": "JDK, JRE, and JVM",
                "order": 4,
                "theory": """JDK, JRE, and JVM are three important parts of the Java ecosystem.

JVM stands for Java Virtual Machine. It is the engine that runs Java bytecode. The JVM makes Java platform independent because the same bytecode can run on different operating systems as long as the JVM is available.

JRE stands for Java Runtime Environment. It includes the JVM and the libraries needed to run Java applications. If a user only wants to run Java programs, the JRE is enough.

JDK stands for Java Development Kit. It includes the JRE along with development tools such as the Java compiler, debugger, and other utilities. If a developer wants to write and compile Java programs, the JDK is required.

In short:
- JVM runs the program
- JRE provides the runtime environment
- JDK provides everything needed for development

Understanding the difference between these three is one of the first important topics in Core Java.""",
                "practice_note": "Create a table comparing JDK, JRE, and JVM with purpose, users, and included tools.",
            },
            {
                "title": "Java Tokens, Datatypes, and Variables",
                "order": 5,
                "theory": """A Java program is made of small meaningful elements called tokens. Tokens include keywords, identifiers, literals, operators, and separators.

Datatypes define what kind of value a variable can store. Java has two main datatype groups:
- Primitive datatypes: byte, short, int, long, float, double, char, boolean
- Non-primitive datatypes: String, arrays, classes, interfaces, and objects

A variable is a named memory location used to store data. Each variable must be declared with a datatype before use.

Examples:
- int age = 20;
- double price = 99.5;
- char grade = 'A';
- boolean isPassed = true;

Variable naming should be meaningful and follow Java naming conventions. Good variable names improve readability and reduce confusion in larger programs.

This topic is important because variables and datatypes form the base of almost every Java program.""",
                "syntax_example": """int age = 21;
double cgpa = 8.7;
char section = 'A';
boolean placed = false;
String name = "Ravi";""",
                "practice_note": "Declare variables for student name, age, grade, fee amount, and placement status in Java.",
            },
            {
                "title": "Java Operators",
                "order": 6,
                "theory": """Operators are symbols used to perform operations on values and variables in Java.

Main categories of operators:
- Arithmetic operators: +, -, *, /, %
- Relational operators: ==, !=, >, <, >=, <=
- Logical operators: &&, ||, !
- Assignment operators: =, +=, -=, *=, /=
- Unary operators: ++, --, +, -, !
- Ternary operator: condition ? value1 : value2

Operators are used in calculations, comparisons, conditions, loops, and decision-making logic. Understanding operator precedence is also important because it affects the order in which expressions are evaluated.

For example, multiplication happens before addition unless parentheses are used to change the order.

A good understanding of operators helps in writing correct and efficient Java expressions.""",
                "syntax_example": """int a = 10;
int b = 3;

System.out.println(a + b);
System.out.println(a > b);
System.out.println(a % b);
System.out.println((a > b) && (b > 0));""",
                "practice_note": "Write a Java program that uses arithmetic, relational, and logical operators in one example.",
            },
        ],
    },
    {
        "topic": "Control Statements in Java",
        "summary": "Learn how Java makes decisions and controls program flow using condition-based statements.",
        "level": "beginner",
        "order": 2,
        "lessons": [
            {
                "title": "if, if-else, and nested if",
                "order": 1,
                "theory": """Control statements decide which block of code should execute based on a condition.

The if statement runs a block only when a condition is true. The if-else statement chooses one block when the condition is true and another block when it is false. Nested if statements are used when multiple conditions must be checked in a sequence.

These statements are useful for checking marks, eligibility, login conditions, input validation, and business rules.

Program flow becomes dynamic when decisions are taken at runtime based on data.

Understanding conditional statements is essential because most real-world applications rely on decision making.""",
                "syntax_example": """int marks = 72;

if (marks >= 75) {
    System.out.println("Distinction");
} else if (marks >= 50) {
    System.out.println("Pass");
} else {
    System.out.println("Fail");
}""",
                "practice_note": "Write a Java program to check whether a number is positive, negative, or zero.",
            },
            {
                "title": "switch Statement",
                "order": 2,
                "theory": """The switch statement is used when one variable must be compared against many fixed values.

It makes code easier to read than a long chain of if-else statements when the decision depends on one expression such as a menu option, day number, grade code, or user choice.

Each case represents a possible value. The break statement is usually used to stop execution from continuing into the next case. The default block runs when no case matches.

Switch is especially useful in menu-driven programs and input-based command handling.""",
                "syntax_example": """int day = 2;

switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    case 2:
        System.out.println("Tuesday");
        break;
    default:
        System.out.println("Invalid day");
}""",
                "practice_note": "Create a menu-based program using switch for addition, subtraction, multiplication, and division.",
            },
        ],
    },
    {
        "topic": "OOPS Concepts in Java",
        "summary": "Understand the object-oriented principles that make Java powerful for real-world software development.",
        "level": "intermediate",
        "order": 3,
        "lessons": [
            {
                "title": "Class and Object",
                "order": 1,
                "theory": """A class is a blueprint for creating objects. It defines data members and methods. An object is a real instance of a class created at runtime.

If we compare this to real life, a class is like the design of a car and an object is the actual car built from that design.

Classes help organize code, while objects let programs represent real-world entities such as students, accounts, employees, and products.

This concept is the foundation of Java because Java is primarily an object-oriented language.""",
                "syntax_example": """class Student {
    String name;
    int age;

    void show() {
        System.out.println(name + " " + age);
    }
}

public class Main {
    public static void main(String[] args) {
        Student s1 = new Student();
        s1.name = "Anu";
        s1.age = 21;
        s1.show();
    }
}""",
                "practice_note": "Create a Book class with title and price, then create two objects and display their values.",
            },
            {
                "title": "Inheritance, Polymorphism, Encapsulation, and Abstraction",
                "order": 2,
                "theory": """The four major pillars of object-oriented programming are inheritance, polymorphism, encapsulation, and abstraction.

Inheritance allows one class to acquire the properties and methods of another class. It supports code reuse and hierarchy creation.

Polymorphism allows the same method name to behave differently in different situations. It improves flexibility and supports extensible design.

Encapsulation means wrapping data and methods into one unit and restricting direct access to internal details. It is commonly implemented using private fields and getter-setter methods.

Abstraction means hiding implementation details and showing only essential behavior. It helps developers focus on what an object does instead of how it does it.

These concepts are central to writing maintainable Java applications and are frequently asked in interviews.""",
                "practice_note": "Prepare one example each for inheritance, polymorphism, encapsulation, and abstraction using simple real-life classes.",
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed starter Core Java course content for the learn module."

    def handle(self, *args, **options):
        language, _ = Language.objects.get_or_create(
            name="Core Java",
            defaults={
                "icon": "JAVA",
                "description": "Learn Java from fundamentals to object-oriented concepts with structured modules and lesson-wise reading.",
                "order": 1,
                "color": "#2563EB",
            },
        )

        created_topics = 0
        created_lessons = 0

        for topic_data in JAVA_CONTENT:
            topic, topic_created = Topic.objects.get_or_create(
                language=language,
                title=topic_data["topic"],
                defaults={
                    "summary": topic_data["summary"],
                    "level": topic_data["level"],
                    "order": topic_data["order"],
                },
            )
            if topic_created:
                created_topics += 1
            else:
                topic.summary = topic_data["summary"]
                topic.level = topic_data["level"]
                topic.order = topic_data["order"]
                topic.save(update_fields=["summary", "level", "order"])

            for lesson_data in topic_data["lessons"]:
                lesson, lesson_created = Lesson.objects.get_or_create(
                    topic=topic,
                    title=lesson_data["title"],
                    defaults={
                        "theory": lesson_data["theory"],
                        "syntax_example": lesson_data.get("syntax_example", ""),
                        "practice_note": lesson_data.get("practice_note", ""),
                        "order": lesson_data["order"],
                    },
                )
                if lesson_created:
                    created_lessons += 1
                else:
                    lesson.theory = lesson_data["theory"]
                    lesson.syntax_example = lesson_data.get("syntax_example", "")
                    lesson.practice_note = lesson_data.get("practice_note", "")
                    lesson.order = lesson_data["order"]
                    lesson.save(update_fields=["theory", "syntax_example", "practice_note", "order"])

        self.stdout.write(
            self.style.SUCCESS(
                f"Core Java content ready. Topics created: {created_topics}, lessons created: {created_lessons}."
            )
        )
