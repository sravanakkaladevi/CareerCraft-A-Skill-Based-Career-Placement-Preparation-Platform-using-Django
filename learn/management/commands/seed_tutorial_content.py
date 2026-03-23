from django.core.management.base import BaseCommand

from learn.models import Language, Lesson, Topic


TUTORIAL_CONTENT = []

TUTORIAL_CONTENT.extend(
    [
        {
            "language": {
                "name": "Core Java",
                "icon": "JAVA",
                "description": "Learn Java from fundamentals to object-oriented concepts with structured modules and lesson-wise reading.",
                "order": 1,
                "color": "#2563EB",
            },
            "topics": [
                {
                    "title": "Basics of Java",
                    "summary": "Start with Java fundamentals, history, platform basics, variables, and operators.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "What is Java",
                            "order": 1,
                            "theory": "Java is a high-level, object-oriented programming language known for portability, security, and reliability. Java programs are compiled into bytecode and executed by the Java Virtual Machine, which allows the same program to run on different operating systems. Java is widely used in enterprise software, backend systems, Android development, and academic learning.",
                            "syntax_example": 'public class Main {\\n    public static void main(String[] args) {\\n        System.out.println("Hello, Java!");\\n    }\\n}',
                            "practice_note": "Write a Java program to print your name, branch, and college name.",
                        },
                        {
                            "title": "JDK, JRE, and JVM",
                            "order": 2,
                            "theory": "JVM runs Java bytecode. JRE provides the runtime environment required to execute Java applications. JDK includes the JRE plus tools like the compiler and debugger needed for development. In short, JVM executes, JRE runs, and JDK develops.",
                            "syntax_example": "",
                            "practice_note": "Create a comparison table showing the role of JDK, JRE, and JVM.",
                        },
                        {
                            "title": "Variables, Datatypes, and Operators",
                            "order": 3,
                            "theory": "Variables store data, datatypes define what kind of data can be stored, and operators perform actions on that data. Java supports primitive types like int, double, char, and boolean, along with non-primitive types such as String and arrays.",
                            "syntax_example": "int age = 20;\\ndouble fee = 15000.50;\\nchar grade = 'A';\\nboolean isPlaced = false;\\nSystem.out.println(age + 5);",
                            "practice_note": "Declare five variables of different datatypes and print them.",
                        },
                    ],
                },
                {
                    "title": "Control Statements in Java",
                    "summary": "Learn branching and decision-making logic using conditions and switches.",
                    "level": "beginner",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "if, if-else, and nested if",
                            "order": 1,
                            "theory": "Conditional statements control the flow of execution. The if statement runs a block when a condition is true. if-else adds an alternative path, and nested if handles multi-level decisions.",
                            "syntax_example": 'int marks = 76;\\nif (marks >= 75) {\\n    System.out.println("Distinction");\\n} else if (marks >= 50) {\\n    System.out.println("Pass");\\n} else {\\n    System.out.println("Fail");\\n}',
                            "practice_note": "Write a Java program to check whether a year is a leap year or not.",
                        },
                        {
                            "title": "switch Statement",
                            "order": 2,
                            "theory": "The switch statement is useful when a single expression needs to be compared against multiple fixed values. It improves readability in menu-based and category-based programs.",
                            "syntax_example": 'int choice = 2;\\nswitch (choice) {\\n    case 1:\\n        System.out.println("Add");\\n        break;\\n    case 2:\\n        System.out.println("Delete");\\n        break;\\n    default:\\n        System.out.println("Invalid option");\\n}',
                            "practice_note": "Build a simple menu-driven calculator using switch.",
                        },
                    ],
                },
                {
                    "title": "OOPS Concepts in Java",
                    "summary": "Understand classes, objects, inheritance, polymorphism, encapsulation, and abstraction.",
                    "level": "intermediate",
                    "order": 3,
                    "lessons": [
                        {
                            "title": "Class and Object",
                            "order": 1,
                            "theory": "A class is a blueprint, and an object is an instance of that blueprint. In Java, classes define properties and behaviors, while objects represent real-world entities created from classes.",
                            "syntax_example": 'class Student {\\n    String name;\\n    void show() {\\n        System.out.println(name);\\n    }\\n}\\n\\nStudent s = new Student();\\ns.name = "Ravi";\\ns.show();',
                            "practice_note": "Create an Employee class with name and salary fields, then create two objects.",
                        },
                        {
                            "title": "Inheritance, Polymorphism, Encapsulation, and Abstraction",
                            "order": 2,
                            "theory": "Inheritance enables code reuse, polymorphism allows one interface to support many forms, encapsulation protects internal state, and abstraction hides implementation details. These four pillars form the foundation of Java OOP design.",
                            "syntax_example": 'class Animal {\\n    void sound() {\\n        System.out.println("Animal sound");\\n    }\\n}\\nclass Dog extends Animal {\\n    @Override\\n    void sound() {\\n        System.out.println("Bark");\\n    }\\n}',
                            "practice_note": "Write one real-world example for each OOP pillar.",
                        },
                    ],
                },
            ],
        },
        {
            "language": {
                "name": "Advanced Java",
                "icon": "AJAVA",
                "description": "Move into database connectivity, servlets, JSP, and enterprise-oriented Java development.",
                "order": 2,
                "color": "#1d4ed8",
            },
            "topics": [
                {
                    "title": "JDBC",
                    "summary": "Connect Java applications to relational databases and perform CRUD operations.",
                    "level": "intermediate",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "Introduction to JDBC",
                            "order": 1,
                            "theory": "JDBC stands for Java Database Connectivity. It is an API that allows Java applications to connect with databases, execute SQL statements, and process results. JDBC is commonly used for storing and retrieving application data.",
                            "syntax_example": 'Connection con = DriverManager.getConnection(url, username, password);\\nStatement st = con.createStatement();\\nResultSet rs = st.executeQuery("SELECT * FROM students");',
                            "practice_note": "Write the basic steps involved in establishing a JDBC connection.",
                        },
                        {
                            "title": "PreparedStatement and CRUD",
                            "order": 2,
                            "theory": "PreparedStatement is a safer and more efficient way to execute parameterized SQL queries. It helps prevent SQL injection and is used heavily in insert, update, delete, and search operations.",
                            "syntax_example": 'PreparedStatement ps = con.prepareStatement("INSERT INTO students(name, age) VALUES (?, ?)");\\nps.setString(1, "Anu");\\nps.setInt(2, 21);\\nps.executeUpdate();',
                            "practice_note": "Create a student record insertion example using PreparedStatement.",
                        },
                    ],
                },
                {
                    "title": "Servlets and JSP",
                    "summary": "Understand request handling and dynamic page generation in Java web applications.",
                    "level": "intermediate",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "What is a Servlet",
                            "order": 1,
                            "theory": "A Servlet is a server-side Java program that handles requests and generates responses. It is commonly used in web applications to process form data, manage sessions, and control navigation.",
                            "syntax_example": '@WebServlet("/hello")\\npublic class HelloServlet extends HttpServlet {\\n    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {\\n        response.getWriter().println("Hello from Servlet");\\n    }\\n}',
                            "practice_note": "Write a simple servlet that prints a welcome message in the browser.",
                        },
                        {
                            "title": "JSP Basics",
                            "order": 2,
                            "theory": "JSP stands for JavaServer Pages. It allows HTML and Java to work together for dynamic web page generation. JSP is useful for displaying dynamic content returned by backend logic.",
                            "syntax_example": '<html>\\n<body>\\n<h2>Welcome, <%= request.getParameter("name") %></h2>\\n</body>\\n</html>',
                            "practice_note": "Create a JSP page that displays a user name passed from a form.",
                        },
                    ],
                },
            ],
        },
    ]
)

TUTORIAL_CONTENT.extend(
    [
        {
            "language": {
                "name": "C Programming",
                "icon": "C",
                "description": "Learn procedural programming, memory concepts, and efficient problem-solving with C.",
                "order": 6,
                "color": "#1e40af",
            },
            "topics": [
                {
                    "title": "C Basics",
                    "summary": "Start with C syntax, structure, datatypes, variables, and operators.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "Introduction to C",
                            "order": 1,
                            "theory": "C is a general-purpose procedural programming language developed by Dennis Ritchie. It is known for performance, low-level memory access, and strong use in operating systems, embedded systems, and foundational programming education.",
                            "syntax_example": '#include <stdio.h>\\nint main() {\\n    printf("Hello, C");\\n    return 0;\\n}',
                            "practice_note": "Write a C program to print your name and city.",
                        },
                        {
                            "title": "Variables, Datatypes, and Operators in C",
                            "order": 2,
                            "theory": "Variables store values, datatypes define storage format, and operators are used to perform arithmetic, comparison, and logical operations. C supports int, float, char, double, and more.",
                            "syntax_example": "int age = 20;\\nfloat cgpa = 8.5;\\nchar grade = 'A';\\nprintf(\"%d %.1f %c\", age, cgpa, grade);",
                            "practice_note": "Declare variables for roll number, marks, and grade and display them.",
                        },
                    ],
                },
                {
                    "title": "Pointers and Functions",
                    "summary": "Understand reusable logic and direct memory handling with functions and pointers.",
                    "level": "intermediate",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "Functions in C",
                            "order": 1,
                            "theory": "Functions divide a program into smaller reusable parts. They improve readability, modularity, and maintainability. Functions can take arguments and return values.",
                            "syntax_example": 'int add(int a, int b) {\\n    return a + b;\\n}\\n\\nprintf("%d", add(2, 3));',
                            "practice_note": "Write a function to calculate the factorial of a number.",
                        },
                        {
                            "title": "Pointers in C",
                            "order": 2,
                            "theory": "Pointers store memory addresses. They are one of the most powerful features of C and are used in arrays, functions, dynamic memory, and system-level programming.",
                            "syntax_example": 'int x = 10;\\nint *ptr = &x;\\nprintf("%d", *ptr);',
                            "practice_note": "Write a program showing a variable value, address, and value through pointer dereferencing.",
                        },
                    ],
                },
            ],
        },
        {
            "language": {
                "name": "C++",
                "icon": "CPP",
                "description": "Learn high-performance programming with object-oriented features, STL, and problem-solving patterns.",
                "order": 7,
                "color": "#1d4ed8",
            },
            "topics": [
                {
                    "title": "C++ Basics",
                    "summary": "Understand syntax, variables, input-output, and operators in C++.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "Introduction to C++",
                            "order": 1,
                            "theory": "C++ is a general-purpose programming language built as an extension of C with support for object-oriented programming, performance, and system-level development. It is used in games, compilers, competitive programming, and high-performance systems.",
                            "syntax_example": '#include <iostream>\\nusing namespace std;\\nint main() {\\n    cout << "Hello, C++";\\n    return 0;\\n}',
                            "practice_note": "Write a C++ program to print your name and age.",
                        },
                        {
                            "title": "Variables, Input, and Operators",
                            "order": 2,
                            "theory": "C++ variables hold values, cin reads input, and cout prints output. Operators are used for calculations, comparisons, and logical expressions in everyday programs.",
                            "syntax_example": 'int a, b;\\ncin >> a >> b;\\ncout << a + b;',
                            "practice_note": "Take two numbers as input and print their sum, difference, and product.",
                        },
                    ],
                },
                {
                    "title": "OOP and STL",
                    "summary": "Move from procedural logic to classes, objects, and standard template library containers.",
                    "level": "intermediate",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "Classes and Objects in C++",
                            "order": 1,
                            "theory": "C++ supports object-oriented programming through classes and objects. Classes group data and methods together and help model real-world entities cleanly.",
                            "syntax_example": 'class Student {\\npublic:\\n    string name;\\n    void show() {\\n        cout << name;\\n    }\\n};',
                            "practice_note": "Create a Product class with name and price and display both using an object.",
                        },
                        {
                            "title": "vector and pair in STL",
                            "order": 2,
                            "theory": "The Standard Template Library provides ready-made data structures and algorithms. vector is a dynamic array, and pair stores two related values together.",
                            "syntax_example": 'vector<int> nums = {1, 2, 3};\\npair<string, int> p = {"Ravi", 21};\\ncout << nums[0] << " " << p.first;',
                            "practice_note": "Create a vector of five integers and print all values using a loop.",
                        },
                    ],
                },
            ],
        },
        {
            "language": {
                "name": "MySQL",
                "icon": "SQL",
                "description": "Learn relational databases, SQL queries, joins, constraints, and practical data handling.",
                "order": 8,
                "color": "#0369a1",
            },
            "topics": [
                {
                    "title": "SQL Basics",
                    "summary": "Start with databases, tables, rows, and essential SQL commands.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "What is MySQL",
                            "order": 1,
                            "theory": "MySQL is a relational database management system used to store, manage, and retrieve structured data. It is widely used in web applications, business systems, analytics tools, and backend development.",
                            "syntax_example": 'CREATE DATABASE college;\\nUSE college;',
                            "practice_note": "Write the difference between a database, table, row, and column.",
                        },
                        {
                            "title": "CREATE, INSERT, SELECT",
                            "order": 2,
                            "theory": "These are the most basic SQL operations. CREATE defines the table structure, INSERT adds new records, and SELECT retrieves stored data from the table.",
                            "syntax_example": 'CREATE TABLE students (\\n    id INT,\\n    name VARCHAR(50)\\n);\\nINSERT INTO students VALUES (1, "Anu");\\nSELECT * FROM students;',
                            "practice_note": "Create an employee table and insert three sample records.",
                        },
                    ],
                },
                {
                    "title": "Filtering and Joins",
                    "summary": "Retrieve exactly the data you need using conditions and relational joins.",
                    "level": "intermediate",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "WHERE, ORDER BY, GROUP BY",
                            "order": 1,
                            "theory": "WHERE filters records, ORDER BY sorts them, and GROUP BY combines rows for aggregate operations. These commands are essential for reporting and analysis queries.",
                            "syntax_example": 'SELECT department, COUNT(*)\\nFROM employees\\nWHERE salary > 30000\\nGROUP BY department\\nORDER BY department;',
                            "practice_note": "Write a query to show departments and employee count sorted by department name.",
                        },
                        {
                            "title": "INNER JOIN and LEFT JOIN",
                            "order": 2,
                            "theory": "Joins combine data from multiple tables. INNER JOIN returns only matching rows, while LEFT JOIN returns all rows from the left table even if no match exists in the right table.",
                            "syntax_example": 'SELECT s.name, d.dept_name\\nFROM students s\\nINNER JOIN departments d ON s.dept_id = d.id;',
                            "practice_note": "Create an example using two tables and explain the difference between INNER JOIN and LEFT JOIN.",
                        },
                    ],
                },
            ],
        },
    ]
)

TUTORIAL_CONTENT.extend(
    [
        {
            "language": {
                "name": "Python",
                "icon": "PY",
                "description": "Learn Python from syntax and data types to functions, OOP, and practical programming.",
                "order": 3,
                "color": "#0f766e",
            },
            "topics": [
                {
                    "title": "Python Basics",
                    "summary": "Start with syntax, variables, datatypes, and input-output basics in Python.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "What is Python",
                            "order": 1,
                            "theory": "Python is a high-level, interpreted, easy-to-read programming language. It is widely used in web development, automation, data science, machine learning, and scripting. Python is beginner-friendly because its syntax is close to plain English.",
                            "syntax_example": 'print("Hello, Python!")',
                            "practice_note": "Write a Python program to print your name and favorite subject.",
                        },
                        {
                            "title": "Variables and Datatypes",
                            "order": 2,
                            "theory": "Python variables are created when values are assigned. Common datatypes include int, float, str, bool, list, tuple, dict, and set. Python does not require explicit datatype declarations for normal variables.",
                            "syntax_example": 'name = "Anu"\\nage = 20\\ncgpa = 8.5\\nis_placed = False\\nprint(name, age, cgpa, is_placed)',
                            "practice_note": "Create variables for student name, age, branch, and grade, then print them.",
                        },
                    ],
                },
                {
                    "title": "Functions and OOP in Python",
                    "summary": "Learn reusable code with functions and understand object-oriented programming basics.",
                    "level": "intermediate",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "Functions in Python",
                            "order": 1,
                            "theory": "Functions are reusable blocks of code that perform a specific task. They help break large programs into smaller manageable parts and improve readability and reuse.",
                            "syntax_example": 'def add(a, b):\\n    return a + b\\n\\nprint(add(5, 3))',
                            "practice_note": "Write a function that returns the square of a number.",
                        },
                        {
                            "title": "Classes and Objects in Python",
                            "order": 2,
                            "theory": "Python supports object-oriented programming through classes and objects. A class defines structure and behavior, while objects are instances created from that class.",
                            "syntax_example": 'class Student:\\n    def __init__(self, name):\\n        self.name = name\\n\\n    def show(self):\\n        print(self.name)\\n\\ns = Student("Ravi")\\ns.show()',
                            "practice_note": "Create a Car class with brand and model and print both using a method.",
                        },
                    ],
                },
            ],
        },
        {
            "language": {
                "name": "DSA",
                "icon": "DSA",
                "description": "Build strong problem-solving skills with data structures, algorithms, and complexity analysis.",
                "order": 4,
                "color": "#7c3aed",
            },
            "topics": [
                {
                    "title": "DSA Introduction",
                    "summary": "Understand the purpose of data structures and algorithms and why they matter.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "Why Learn DSA",
                            "order": 1,
                            "theory": "DSA helps you solve problems efficiently, write optimized code, and prepare for technical interviews. It teaches how to store data properly and how to design step-by-step solutions for real-world problems.",
                            "syntax_example": "",
                            "practice_note": "Write three reasons why DSA is important for placements and interviews.",
                        },
                        {
                            "title": "What is an Algorithm",
                            "order": 2,
                            "theory": "An algorithm is a finite set of well-defined steps used to solve a problem. A good algorithm should be correct, efficient, and understandable.",
                            "syntax_example": 'Algorithm to find maximum:\\n1. Assume first element is max\\n2. Compare it with remaining elements\\n3. Update max when needed\\n4. Print max',
                            "practice_note": "Write an algorithm to find the largest of three numbers.",
                        },
                    ],
                },
                {
                    "title": "Linear Data Structures",
                    "summary": "Study arrays, linked lists, stacks, and queues used in day-to-day programming problems.",
                    "level": "intermediate",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "Arrays",
                            "order": 1,
                            "theory": "An array stores elements of the same datatype in contiguous memory locations. Arrays allow fast indexed access and are useful when the number of elements is fixed or known in advance.",
                            "syntax_example": 'arr = [10, 20, 30, 40]\\nprint(arr[2])',
                            "practice_note": "Write a program to find the sum of all elements in an array.",
                        },
                        {
                            "title": "Stack and Queue Basics",
                            "order": 2,
                            "theory": "A stack follows LIFO, meaning the last inserted element is removed first. A queue follows FIFO, meaning the first inserted element is removed first. Both are useful in scheduling, parsing, and traversal problems.",
                            "syntax_example": 'stack = []\\nstack.append(10)\\nstack.append(20)\\nprint(stack.pop())',
                            "practice_note": "Write the difference between stack and queue with one real-life example each.",
                        },
                    ],
                },
            ],
        },
        {
            "language": {
                "name": "HTML",
                "icon": "HTML",
                "description": "Build strong web page structure using HTML elements, forms, tables, and semantic tags.",
                "order": 5,
                "color": "#ea580c",
            },
            "topics": [
                {
                    "title": "HTML Basics",
                    "summary": "Learn the structure of HTML documents and common tags used in web pages.",
                    "level": "beginner",
                    "order": 1,
                    "lessons": [
                        {
                            "title": "What is HTML",
                            "order": 1,
                            "theory": "HTML stands for HyperText Markup Language. It is the standard markup language used to create and structure web pages. HTML defines headings, paragraphs, links, images, tables, forms, and many other visible page elements.",
                            "syntax_example": '<!DOCTYPE html>\\n<html>\\n<head>\\n    <title>My Page</title>\\n</head>\\n<body>\\n    <h1>Hello World</h1>\\n</body>\\n</html>',
                            "practice_note": "Create a basic HTML page with your name in a heading and a short introduction in a paragraph.",
                        },
                        {
                            "title": "Text, Links, and Images",
                            "order": 2,
                            "theory": "HTML provides tags for text formatting, anchor links, and image embedding. These are the core building blocks of informational web pages.",
                            "syntax_example": '<h2>About Me</h2>\\n<p>I love web development.</p>\\n<a href="https://example.com">Visit Site</a>\\n<img src="profile.jpg" alt="Profile Image">',
                            "practice_note": "Build a mini profile page with one heading, one paragraph, one link, and one image.",
                        },
                    ],
                },
                {
                    "title": "Forms and Tables",
                    "summary": "Create interactive forms and present structured information using tables.",
                    "level": "beginner",
                    "order": 2,
                    "lessons": [
                        {
                            "title": "HTML Forms",
                            "order": 1,
                            "theory": "Forms are used to collect user input. Common form elements include input fields, labels, textareas, radio buttons, checkboxes, dropdowns, and buttons.",
                            "syntax_example": '<form>\\n    <label>Name</label>\\n    <input type="text" name="name">\\n    <button type="submit">Submit</button>\\n</form>',
                            "practice_note": "Create a student registration form with name, email, branch, and submit button.",
                        },
                        {
                            "title": "HTML Tables",
                            "order": 2,
                            "theory": "Tables are used to display data in rows and columns. They are useful for marksheets, schedules, reports, and structured comparison views.",
                            "syntax_example": '<table border="1">\\n    <tr><th>Name</th><th>Marks</th></tr>\\n    <tr><td>Ana</td><td>92</td></tr>\\n</table>',
                            "practice_note": "Create a marks table for three students with columns for name and score.",
                        },
                    ],
                },
            ],
        },
    ]
)


def _upsert_content():
    created_topics = 0
    created_lessons = 0

    for language_block in TUTORIAL_CONTENT:
        language_data = language_block["language"]
        language, _ = Language.objects.get_or_create(
            name=language_data["name"],
            defaults={
                "icon": language_data["icon"],
                "description": language_data["description"],
                "order": language_data["order"],
                "color": language_data["color"],
            },
        )

        language.icon = language_data["icon"]
        language.description = language_data["description"]
        language.order = language_data["order"]
        language.color = language_data["color"]
        language.save(update_fields=["icon", "description", "order", "color"])

        for topic_data in language_block["topics"]:
            topic, topic_created = Topic.objects.get_or_create(
                language=language,
                title=topic_data["title"],
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

    return created_topics, created_lessons


class Command(BaseCommand):
    help = "Seed starter tutorial content for major learn tracks."

    def handle(self, *args, **options):
        created_topics, created_lessons = _upsert_content()
        self.stdout.write(
            self.style.SUCCESS(
                f"Tutorial starter content ready. Topics created: {created_topics}, lessons created: {created_lessons}."
            )
        )
