"""Course Learning Outcomes from the department's curriculum documents.

GENERATED from the BSCS / BSSE / BSAI curriculum PDFs (the "Course Learning
Outcomes" section of each course outline), then reviewed. Edit by hand if a
statement needs correcting -- there is no re-generation step.

For each CLO:
* `description` is the outcome statement as printed (whitespace normalised,
  list numbering and "By the end of this course..." lead-ins removed).
* `title` is a short label derived from it (leading action verb dropped).
* `bloom_level` is inferred from the statement's action verb (Describe ->
  Understand, Design -> Create, ...). Faculty can change any of these after
  adding the CLOs to a course.

Courses whose outline has an empty CLO section (or only "As per guidelines of
NCEAC and HEC") have no entry. Outlines printed under a code that belongs to a
different course in the plan (e.g. "Technical and Business Writing (SE-557)")
were matched by name or left out, never attached to the wrong course.

Keyed by programme code, then catalog course code (see app/core/curriculum.py).
BS Data Science uses the BSCS entries via `curriculum.CURRICULUM_SOURCE`.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class CatalogCLO:
    title: str
    description: str
    bloom_level: str


def _clos(*rows: tuple[str, str, str]) -> tuple[CatalogCLO, ...]:
    return tuple(CatalogCLO(title, description, bloom) for title, description, bloom in rows)


CURRICULUM_CLOS: dict[str, dict[str, tuple[CatalogCLO, ...]]] = {
    'BSCS': {
        'CS-351': _clos(
            ('Basic problem-solving steps and logic constructs', 'Understand basic problem-solving steps and logic constructs', 'Understand'),
            ('Basic programing concepts', 'Apply basic programing concepts', 'Apply'),
            ('Design and implement algorithms to solve real world problems', 'Design and implement algorithms to solve real world problems', 'Create'),
        ),
        'CS-352': _clos(
            ('Principles of object-oriented paradigm', 'Understand principles of object-oriented paradigm.', 'Understand'),
            ('Objects & their relationships', 'Identify the objects & their relationships to build object-oriented solution', 'Remember'),
            ('Solution for a given problem', 'Model a solution for a given problem using object-oriented principles', 'Create'),
            ('Object-oriented solution', 'Examine an object-oriented solution', 'Analyze'),
        ),
        'CS-353': _clos(
            ('Basics of computing technology', 'Understand basics of computing technology', 'Understand'),
            ('Number systems conversions and arithmetic', 'Do number systems conversions and arithmetic', 'Apply'),
            ('Types of software', 'Have knowledge of types of software', 'Remember'),
            ('Computing related technologies', 'Have knowledge of computing related technologies', 'Remember'),
        ),
        'CS-354': _clos(
            ('The concepts', 'Acquire knowledge related to the concepts, tools and techniques for the design of digital electronic circuits', 'Remember'),
            ('Demonstrate the skills to design and analyze both combinational and sequential circuits using a variety of techniques', 'Demonstrate the skills to design and analyze both combinational and sequential circuits using a variety of techniques', 'Apply'),
            ('Acquired knowledge to simulate', 'Apply the acquired knowledge to simulate and implement small-scale digital circuits', 'Apply'),
            ('Relationship between abstract logic characterizations and practical electrical implementations', 'Understand the relationship between abstract logic characterizations and practical electrical implementations', 'Understand'),
        ),
        'CS-355': _clos(
            ('Fundamental concepts of differential and integral calculus', 'Understand the fundamental concepts of differential and integral calculus.', 'Understand'),
            ('Apply calculus to solve problems in optimization, curve sketching, and area calculation', 'Apply calculus to solve problems in optimization, curve sketching, and area calculation.', 'Apply'),
            ('Conic sections', 'Analyze and interpret conic sections using analytical geometry.', 'Analyze'),
            ('Calculus concepts in AI applications', 'Utilize calculus concepts in AI applications such as machine learning algorithms, neural networks, and robotics.', 'Apply'),
            ('Problem-solving skills relevant to AI technologies', 'Develop problem-solving skills relevant to AI technologies through mathematical modeling.', 'Create'),
        ),
        'CS-356': _clos(
            ('Vector and matrix operations', 'Understand and manipulate vector and matrix operations.', 'Understand'),
            ('Systems of linear equations', 'Solve systems of linear equations using various methods.', 'Apply'),
            ('Concepts of vector spaces, subspaces, bases, and dimensions', 'Grasp the concepts of vector spaces, subspaces, bases, and dimensions.', 'Understand'),
            ('Eigenvalues and eigenvectors in practical scenarios', 'Apply eigenvalues and eigenvectors in practical scenarios, especially in AI and machine learning models.', 'Apply'),
            ('Linear transformations', 'Use linear transformations to model real-world problems in AI.', 'Apply'),
            ('Linear algebra operations', 'Implement linear algebra operations using computational tools such as Python and MATLAB.', 'Apply'),
        ),
        'CS-357': _clos(
            ('Core physics principles to real-world problems', 'Apply core physics principles to real-world problems', 'Apply'),
            ('Experiments that demonstrate these concepts', 'Conduct experiments that demonstrate these concepts.', 'Apply'),
            ('Analytical skills and effectively communicate scientific ideas', 'Enhance your analytical skills and effectively communicate scientific ideas.', 'Apply'),
        ),
        'CS-358': _clos(
            ('Key concepts of Discrete Structures', 'Understand the key concepts of Discrete Structures such as Sets, Permutations, Relations, Graphs and Trees etc.', 'Understand'),
            ('Formal logic proofs and/or informal', 'Apply formal logic proofs and/or informal, but rigorous, logical reasoning to real problems, such as predicting the behavior of software or solving problems such as puzzles.', 'Apply'),
            ('Discrete structures into other computing problems', 'Apply discrete structures into other computing problems such as formal specification, verification, databases, artificial intelligence, and cryptography.', 'Apply'),
            ('Various discrete structures and their relevance within the context of computer science', 'Differentiate various discrete structures and their relevance within the context of computer science, in the areas of data structures and algorithms, in particular', 'Analyze'),
        ),
        'CS-359': _clos(
            ('Understanding and application of English grammar', 'Enhance their understanding and application of English grammar.', 'Apply'),
            ('Strong vocabulary relevant to academic and professional use', 'Develop a strong vocabulary relevant to academic and professional use.', 'Create'),
            ('Reading comprehension and critical analysis of texts', 'Improve their reading comprehension and critical analysis of texts.', 'Apply'),
            ('Writing skills, focusing on academic and technical writing', 'Strengthen their writing skills, focusing on academic and technical writing.', 'Apply'),
            ('Oral communication', 'Gain confidence in oral communication, including presentations and discussions.', 'Understand'),
            ('Techniques for effective communication in professional environments', 'Learn techniques for effective communication in professional environments.', 'Understand'),
            ('Academic and technical reports', 'Writing academic and technical reports', 'Create'),
        ),
        'CS-361': _clos(
            ('Enhance the knowledge of Islam', 'Enhance the knowledge of Islam.', 'Apply'),
            ('Basic concept of Islam and Quran Pak', 'Understand the basic concept of Islam and Quran Pak.', 'Understand'),
            ('Concept of Haqooq ul ibad in the light of Quran', 'Understand the concept of Haqooq ul ibad in the light of Quran.', 'Understand'),
            ('Importance of Islamic concept about other religions', 'Know the importance of Islamic concept about other religions.', 'Remember'),
        ),
        'CS-362': _clos(
            ('History of Pakistan', 'Educate students about the history of Pakistan', 'Understand'),
            ('Various pillar of the state', 'Educate student about the various pillar of the state', 'Understand'),
            ('Government and politics', 'Educate student Government and politics', 'Understand'),
        ),
        'CS-364': _clos(
            ('Quranic verses', 'Interpret Quranic verses using various methodologies of Tafsir', 'Understand'),
            ('Implications of Quranic teachings in contemporary life', 'Discuss the implications of Quranic teachings in contemporary life', 'Understand'),
            ('Teachings of the Quran in their daily life', 'Adopt and practice the teachings of the Quran in their daily life.', 'Apply'),
        ),
        'CS-451': _clos(
            ('Various data structures and their algorithms', 'Implement various data structures and their algorithms and apply them in implementing simple applications', 'Apply'),
            ('Simple algorithms', 'Analyze simple algorithms and determine their complexities', 'Analyze'),
            ('Data structure to other application domains', 'Apply the knowledge of data structure to other application domains', 'Apply'),
            ('New data structures and algorithms', 'Design new data structures and algorithms to solve problems', 'Create'),
        ),
        'CS-452': _clos(
            ('Fundamental database concepts', 'Explain fundamental database concepts', 'Understand'),
            ('Conceptual, logical and physical database schemas', 'Design conceptual, logical and physical database schemas using different data models', 'Create'),
            ('Functional dependencies and resolve database anomalies by normalizing database tables', 'Identify functional dependencies and resolve database anomalies by normalizing database tables', 'Remember'),
            ('Structured Query Language', 'Use Structured Query Language (SQL) for database definition and manipulation in any DBMS', 'Apply'),
        ),
        'CS-453': _clos(
            ('Various software engineering processes and activates', 'Describe various software engineering processes and activates', 'Understand'),
            ('System modeling techniques', 'Apply the system modeling techniques to model a medium size software system', 'Apply'),
            ('Software quality assurance and testing principles to medium size software systems', 'Apply software quality assurance and testing principles to medium size software systems', 'Apply'),
            ('Key principles and common methods for software project management', 'Discuss key principles and common methods for software project management such as scheduling, size estimation, cost estimation and risk analysis', 'Understand'),
        ),
        'CS-454': _clos(
            ('Fundamental principles of communication', 'Understand the fundamental principles of communication.', 'Understand'),
            ('Effective verbal and non-verbal communication skills', 'Develop effective verbal and non-verbal communication skills.', 'Create'),
            ('Public speaking and presentation abilities', 'Enhance public speaking and presentation abilities.', 'Apply'),
            ('Techniques for professional communication', 'Learn techniques for professional communication, including emails and reports.', 'Understand'),
            ('Delivering technical presentations', 'Build confidence in delivering technical presentations.', 'Create'),
            ('Participating in group discussions, debates, and meetings', 'Improve their skills in participating in group discussions, debates, and meetings.', 'Apply'),
        ),
        'CS-455': _clos(
            ('Computer organization computer architecture and assembly language', 'Acquire the basic knowledge of computer organization computer architecture and assembly language', 'Remember'),
            ('Concepts of basic computer organization, architecture, and assembly language techniques', 'Understand the concepts of basic computer organization, architecture, and assembly language techniques', 'Understand'),
            ('Problems related to computer organization and assembly language', 'Solve the problems related to computer organization and assembly language', 'Apply'),
        ),
        'CS-456': _clos(
            ('Different concepts in automata theory and formal languages', 'Explain and manipulate the different concepts in automata theory and formal languages such as formal proofs, automata, regular expressions, Turing machines etc.', 'Understand'),
            ('Properties of languages', 'Prove properties of languages, grammars and automata with rigorously formal mathematical methods', 'Evaluate'),
            ('Of automata, RE and CFG', 'Design of automata, RE and CFG', 'Create'),
            ('Between equivalent NFAs, DFAs and Res', 'Transform between equivalent NFAs, DFAs and Res', 'Apply'),
            ('Turing machines performing simple tasks', 'Define Turing machines performing simple tasks', 'Remember'),
            ('Formal descriptions of languages', 'Differentiate and manipulate formal descriptions of languages, automata and grammars with focus on regular and context-free languages, finite automata and regular expressions.', 'Analyze'),
        ),
        'CS-458': _clos(
            ('Fundamental project management concepts', 'Explain fundamental project management concepts.', 'Understand'),
            ('Project planning techniques to software projects', 'Apply project planning techniques to software projects.', 'Apply'),
            ('Risks and constraints in project execution', 'Analyze risks and constraints in project execution.', 'Analyze'),
            ('Project management tools', 'Use project management tools to plan and track progress.', 'Apply'),
            ('Leadership and teamwork in simulated project environments', 'Demonstrate leadership and teamwork in simulated project environments.', 'Apply'),
        ),
        'CS-459': _clos(
            ('Basic principles of probability theory', 'Understand and apply the basic principles of probability theory.', 'Understand'),
            ('Analyze data using statistical methods and draw valid conclusions', 'Analyze data using statistical methods and draw valid conclusions.', 'Analyze'),
            ('Probability models', 'Use probability models to describe random processes and uncertainty.', 'Apply'),
            ('Statistical techniques in AI and machine learning problems', 'Apply statistical techniques in AI and machine learning problems.', 'Apply'),
            ('Software tools for statistical analysis and data visualization', 'Use software tools for statistical analysis and data visualization.', 'Apply'),
        ),
        'CS-460': _clos(
            ('Key terminologies and technologies of computer networks', 'Describe the key terminologies and technologies of computer networks', 'Understand'),
            ('Services and functions provided by each layer in the Internet protocol stack', 'Explain the services and functions provided by each layer in the Internet protocol stack', 'Understand'),
            ('Various internetworking devices and protocols and their functions in a networking', 'Identify various internetworking devices and protocols and their functions in a networking', 'Remember'),
            ('Working and performance of key technologies, algorithms and protocols', 'Analyze working and performance of key technologies, algorithms and protocols', 'Analyze'),
        ),
        'CS-462': _clos(
            ('Key skills in ethical decision-making and effective communication in a professional environment', 'Develop key skills in ethical decision-making and effective communication in a professional environment.', 'Create'),
            ('Navigate workplace dynamics', 'Learn how to navigate workplace dynamics and enhance your collaboration and leadership abilities', 'Understand'),
        ),
        'CS-551': _clos(
            ('Fundamental constructs of Python programming language', 'Understand the fundamental constructs of Python programming language', 'Understand'),
            ('Key concepts in the field of artificial intelligence', 'Understand key concepts in the field of artificial intelligence', 'Understand'),
            ('Artificial intelligence techniques and case studies', 'Implement artificial intelligence techniques and case studies', 'Apply'),
        ),
        'CS-552': _clos(
            ('Advance data models', 'Understanding advance data models, technologies and approaches for building distributed database systems.', 'Understand'),
            ('Models and approaches', 'Applying the models and approaches in order to become enabled to select and apply appropriate methods for a particular case', 'Apply'),
            ('Database solution for a given scenario/ challenging problem…', 'Develop a database solution for a given scenario/ challenging problem in the domain of distributed database systems.', 'Create'),
        ),
        'CS-553': _clos(
            ('Characteristics of different structures of the Operating Systems', 'Understand the characteristics of different structures of the Operating Systems and identify the core functions of the Operating Systems', 'Understand'),
            ('Algorithms of the core functions of the Operating Systems', 'Analyze and evaluate the algorithms of the core functions of the Operating Systems and explain the major performance issues with regard to the core functions', 'Analyze'),
            ('Applying system software and tools available in modern operating systems', 'Demonstrate the knowledge in applying system software and tools available in modern operating systems.', 'Apply'),
        ),
        'CS-554': _clos(
            ('Basic techniques used in compiler construction', 'Understand the basic techniques used in compiler construction such as lexical analysis, top-down, bottom-up parsing, context-sensitive analysis, and intermediate code Generation', 'Understand'),
            ('Basic data structures used in compiler construction', 'Understand the basic data structures used in compiler construction such as abstract syntax trees, symbol tables, three-address code, and stack machines', 'Understand'),
            ('Design and implement a compiler using a software engineering approach', 'Design and implement a compiler using a software engineering approach', 'Create'),
            ('Use generators (e.g. Lex and Yacc)', 'Use generators (e.g. Lex and Yacc)', 'Apply'),
        ),
        'CS-555': _clos(
            ('Key principles, models, and theories of human-computer interaction', 'Explain key principles, models, and theories of human-computer interaction.', 'Understand'),
            ('Usability issues in user interfaces', 'Analyze and identify usability issues in user interfaces through heuristic evaluation, cognitive walkthroughs, and user studies.', 'Analyze'),
            ('Interactive user interfaces applying usability, accessibility, and visual design principles', 'Design interactive user interfaces applying usability, accessibility, and visual design principles.', 'Create'),
            ('Fundamental graphics concepts', 'Describe fundamental graphics concepts such as rendering pipelines, transformation, clipping, and projection.', 'Understand'),
            ('2D and 3D rendering algorithms', 'Implement 2D and 3D rendering algorithms including shading, lighting, rasterization, and texturing.', 'Apply'),
        ),
        'CS-556': _clos(
            ('What is meant by “best”', 'Explain what is meant by “best”, “expected”, and “worst” case behavior of an algorithm', 'Understand'),
            ('Characteristics of data and/or other conditions or assumptions…', 'Identify the characteristics of data and/or other conditions or assumptions that lead to different behaviors.', 'Remember'),
            ('Informally the time and space complexity of simple algorithms', 'Determine informally the time and space complexity of simple algorithms', 'Analyze'),
            ('Standard complexity classes', 'List and contrast standard complexity classes', 'Remember'),
            ('Big O', 'Use big O, Omega, Theta notation formally to give asymptotic upper bounds on time and space complexity of algorithms', 'Apply'),
            ('Of the strategies', 'Use of the strategies (brute-force, greedy, divide-and- conquer, and dynamic programming) to solve an appropriate problem', 'Apply'),
            ('Solve problems using graph algorithms, including single- source and all-pairs shortest paths, and at least one minimum spanning tree algorithm', 'Solve problems using graph algorithms, including single- source and all-pairs shortest paths, and at least one minimum spanning tree algorithm', 'Apply'),
            ('And/or implement a string-matching algorithm', 'Trace and/or implement a string-matching algorithm', 'Analyze'),
        ),
        'CS-557': _clos(
            ('Key concepts of information security', 'Explain key concepts of information security such as design principles, cryptography, risk management, and ethics', 'Understand'),
            ('Legal, ethical, and professional issues in information security', 'Discuss legal, ethical, and professional issues in information security', 'Understand'),
            ('Various security and risk management tools for achieving information security and privacy', 'Apply various security and risk management tools for achieving information security and privacy', 'Apply'),
            ('Appropriate techniques to tackle', 'Identify appropriate techniques to tackle and solve problems in the discipline of information security', 'Remember'),
        ),
        'CS-559': _clos(
            ('Civic Responsibilities', 'Understand Civic Responsibilities: Explain the principles of civic duty, community involvement, and the roles of government and individuals in society.', 'Understand'),
            ('Social Issues', 'Analyze Social Issues: Identify and analyze pressing social, political, and economic issues within local, national, and global contexts, understanding their impact on communities.', 'Analyze'),
            ('Community-Based Learning', 'Engage in Community-Based Learning: Participate in activities that foster community engagement, applying course concepts to real-world scenarios through volunteer work, community projects, or partnerships.', 'Apply'),
            ('Critical Thinking on Public Policy', 'Develop Critical Thinking on Public Policy: Evaluate public policies and proposals, considering their implications for social justice, equity, and community well-being.', 'Create'),
            ('Effective Communication and Advocacy', 'Practice Effective Communication and Advocacy: Demonstrate skills in communicating ideas, advocating for community needs, and engaging with diverse audiences through written, oral, and digital means.', 'Apply'),
            ('Personal and Social Impact', 'Reflect on Personal and Social Impact: Assess personal values and actions in relation to civic responsibilities, exploring how individual contributions can promote positive social change.', 'Evaluate'),
            ('Community Solutions', 'Collaborate for Community Solutions: Work collaboratively on community-based projects, developing strategies to address social issues and strengthen community resilience.', 'Apply'),
        ),
        'CS-561': _clos(
            ('Fundamental cloud computing models and services', 'Describe fundamental cloud computing models and services (IaaS, PaaS, SaaS).', 'Understand'),
            ('And manage applications in cloud environments', 'Deploy and manage applications in cloud environments.', 'Apply'),
            ('Benefits and challenges of cloud computing', 'Analyze the benefits and challenges of cloud computing.', 'Analyze'),
            ('Basic cloud security and compliance measures', 'Implement basic cloud security and compliance measures.', 'Apply'),
            ('Cloud solutions for scalability, cost, and performance', 'Evaluate cloud solutions for scalability, cost, and performance.', 'Evaluate'),
        ),
        'CS-572': _clos(
            ('Advanced object-oriented and functional programming concepts', 'Apply advanced object-oriented and functional programming concepts to develop robust software solutions.', 'Apply'),
            ('Multithreaded and concurrent programs with proper synchronization and performance considerations', 'Develop multithreaded and concurrent programs with proper synchronization and performance considerations.', 'Create'),
            ('Exception handling, file operations, and database connectivity in complex programs', 'Utilize exception handling, file operations, and database connectivity in complex programs.', 'Apply'),
            ('Design patterns, modular programming, and best practices', 'Apply design patterns, modular programming, and best practices to enhance code maintainability and reusability.', 'Apply'),
            ('Debug, and optimize software for efficiency, scalability, and resource management', 'Analyze, debug, and optimize software for efficiency, scalability, and resource management.', 'Analyze'),
            ('Advanced programming concepts into real-world mini-projects and case studies', 'Integrate advanced programming concepts into real-world mini-projects and case studies.', 'Create'),
        ),
        'CS-574': _clos(
            ('Different architectures & framework for Mobile Application development', 'Discuss different architectures & framework for Mobile Application development.', 'Understand'),
            ('Mobile applications', 'Develop mobile applications using current software development environments.', 'Create'),
            ('Different performance tradeoffs in mobile application development', 'Compare the different performance tradeoffs in mobile application development.', 'Analyze'),
        ),
        'CS-575': _clos(
            ('Principles and protocols underlying web technologies', 'Explain the principles and protocols underlying web technologies, including HTTP, HTML, CSS, and JavaScript.', 'Understand'),
            ('Dynamic web applications', 'Develop dynamic web applications using client-side and server-side programming techniques.', 'Create'),
            ('Best practices in web application architecture, scalability, and performance optimization', 'Apply best practices in web application architecture, scalability, and performance optimization.', 'Apply'),
            ('Modern frameworks, libraries, and tools', 'Utilize modern frameworks, libraries, and tools to develop robust and maintainable web applications.', 'Apply'),
            ('Web security principles', 'Understand web security principles and implement measures to protect web applications from common threats.', 'Understand'),
            ('Web applications to ensure functionality, usability, and cross-platform compatibility', 'Evaluate and debug web applications to ensure functionality, usability, and cross-platform compatibility.', 'Evaluate'),
        ),
        'CS-576': _clos(
            ('Different multimedia data types, formats, and standards', 'Understand and describe different multimedia data types, formats, and standards.', 'Understand'),
            ('Multimedia compression, storage, and retrieval techniques effectively', 'Apply multimedia compression, storage, and retrieval techniques effectively.', 'Apply'),
            ('Interactive multimedia applications', 'Design and develop interactive multimedia applications using appropriate tools and technologies.', 'Create'),
            ('Multimedia system architectures', 'Analyze multimedia system architectures and implement efficient multimedia communication.', 'Analyze'),
            ('Multimedia systems for usability', 'Evaluate multimedia systems for usability, performance, and quality across various application domains.', 'Evaluate'),
        ),
        'CS-577': _clos(
            ('Principles of simulation and digital twin technology and their applications…', 'Explain the principles of simulation and digital twin technology and their applications in computer science.', 'Understand'),
            ('Digital twin models or simulation scenarios', 'Design and implement digital twin models or simulation scenarios using simulation frameworks.', 'Create'),
            ('Interactive elements', 'Integrate interactive elements, physics, and real-time behavior into simulations or digital twins.', 'Create'),
            ('Simulation and digital twin performance', 'Analyze simulation and digital twin performance, accuracy, and user interaction for refinement.', 'Analyze'),
        ),
        'CS-578': _clos(
            ('Object-oriented principles', 'Apply object-oriented principles to model, analyze, and design software systems.', 'Apply'),
            ('Requirements engineering', 'Perform requirements engineering using use cases and prototyping.', 'Apply'),
            ('Class, interaction', 'Develop and interpret class, interaction, and state diagrams for system behavior.', 'Create'),
            ('Design patterns and architectural principles', 'Apply design patterns and architectural principles to create maintainable software.', 'Apply'),
            ('OO designs to ensure correctness, quality, and scalability', 'Verify and validate OO designs to ensure correctness, quality, and scalability.', 'Evaluate'),
        ),
        'CS-651': _clos(
            ('About parallel and distributed computers', 'Learn about parallel and distributed computers.', 'Understand'),
            ('Portable programs for parallel or distributed-architectures', 'Write portable programs for parallel or distributed-architectures using Message-Passing Interface (MPI) Library', 'Apply'),
            ('Complex problems with shared memory-programming with openMP', 'Analyze complex problems with shared memory-programming with openMP', 'Analyze'),
        ),
        'CS-653': _clos(
            ('Fundamental concepts and principles of entrepreneurship', 'Explain the fundamental concepts and principles of entrepreneurship.', 'Understand'),
            ('Business opportunities', 'Identify and evaluate business opportunities and develop innovative ideas.', 'Remember'),
            ('Basic business plans', 'Prepare basic business plans, including financial, marketing, and operational strategies.', 'Apply'),
            ('Legal, ethical, and social responsibilities in business', 'Demonstrate knowledge of legal, ethical, and social responsibilities in business.', 'Apply'),
            ('Entrepreneurial thinking and problem-solving skills to start or manage small businesses successfully', 'Apply entrepreneurial thinking and problem-solving skills to start or manage small businesses successfully.', 'Apply'),
        ),
        'CS-671': _clos(
            ('Principles of software testing and quality assurance', 'Explain the principles of software testing and quality assurance, including standards and best practices.', 'Understand'),
            ('Various testing strategies', 'Design and implement various testing strategies, such as unit, integration, system, and acceptance testing.', 'Create'),
            ('Automated testing tools and techniques', 'Apply automated testing tools and techniques to improve testing efficiency and coverage.', 'Apply'),
            ('Document, and manage software defects effectively', 'Identify, document, and manage software defects effectively.', 'Remember'),
            ('Quality assurance practices into the software development lifecycle…', 'Integrate quality assurance practices into the software development lifecycle to ensure reliable and maintainable software.', 'Create'),
        ),
        'CS-672': _clos(
            ('Structure of modern computer graphics systems', 'Comprehend the structure of modern computer graphics systems', 'Understand'),
            ('Basic principles of implementing computer graphics fundamentals', 'Explain the basic principles of implementing computer graphics fundamentals', 'Understand'),
            ('Key algorithms for modelling and rendering graphical data', 'Compare key algorithms for modelling and rendering graphical data', 'Analyze'),
            ('Design and problem-solving skills with applications to computer graphics', 'Develop design and problem-solving skills with applications to computer graphics', 'Create'),
            ('Interactive computer graphics programs', 'Construct interactive computer graphics programs using OpenGL', 'Create'),
        ),
        'CS-673': _clos(
            ('Basic security concepts, terminology, and malware classifications', 'Explain basic security concepts, terminology, and malware classifications.', 'Understand'),
            ('And mitigate common attacks on web applications', 'Identify and mitigate common attacks on web applications, including SQL injection, XSS, and CSRF.', 'Remember'),
            ('Network protocols, service models', 'Understand network protocols, service models, and apply transport and network layer security measures.', 'Understand'),
            ('Security measures for wireless networks, cloud services, and IoT devices', 'Implement security measures for wireless networks, cloud services, and IoT devices.', 'Apply'),
            ('About basic security planning and policies to protect information and systems', 'Learn about basic security planning and policies to protect information and systems.', 'Understand'),
        ),
        'CS-674': _clos(
            ('Fundamental principles of data science', 'Understand the fundamental principles of data science.', 'Understand'),
            ('EDA and the Data Science processes', 'Apply EDA and the Data Science processes.', 'Apply'),
            ('Basic machine learning algorithms', 'Apply basic machine learning algorithms to solve real-world problems of moderate complexity.', 'Apply'),
        ),
        'CS-677': _clos(
            ('How web standards impact software development', 'Discuss how web standards impact software development.', 'Understand'),
            ('Constraints that the web puts on developers', 'Describe the constraints that the web puts on developers.', 'Understand'),
            ('Simple web application', 'Design and implement a simple web application.', 'Create'),
            ('Existing web application against a current web standard', 'Review an existing web application against a current web standard.', 'Understand'),
        ),
    },
    'BSSE': {
        'SE-351': _clos(
            ('Basic problem-solving steps and logic constructs', 'Understand basic problem-solving steps and logic constructs', 'Understand'),
            ('Basic programing concepts', 'Apply basic programing concepts', 'Apply'),
            ('Design and implement algorithms to solve real world problems', 'Design and implement algorithms to solve real world problems', 'Create'),
        ),
        'SE-352': _clos(
            ('Principles of object-oriented paradigm', 'Understand principles of object-oriented paradigm.', 'Understand'),
            ('Objects & their relationships', 'Identify the objects & their relationships to build object-oriented solution', 'Remember'),
            ('Solution for a given problem', 'Model a solution for a given problem using object-oriented principles', 'Create'),
            ('Object-oriented solution', 'Examine an object-oriented solution', 'Analyze'),
        ),
        'SE-353': _clos(
            ('Basics of computing technology', 'Understand basics of computing technology', 'Understand'),
            ('Number systems conversions and arithmetic', 'Do number systems conversions and arithmetic', 'Apply'),
            ('Types of software', 'Have knowledge of types of software', 'Remember'),
            ('Computing related technologies', 'Have knowledge of computing related technologies', 'Remember'),
        ),
        'SE-354': _clos(
            ('Various software engineering processes and activates', 'Describe various software engineering processes and activates', 'Understand'),
            ('System modeling techniques', 'Apply the system modeling techniques to model a medium size software system', 'Apply'),
            ('Software quality assurance and testing principles to medium size software systems', 'Apply software quality assurance and testing principles to medium size software systems', 'Apply'),
            ('Key principles and common methods for software project management', 'Discuss key principles and common methods for software project management such as scheduling, size estimation, cost estimation and risk analysis', 'Understand'),
        ),
        'SE-356': _clos(
            ('Good understanding of the concepts and methods of multivariate calculus', 'Provide students with a good understanding of the concepts and methods of multivariate calculus, described in detail in the syllabus.', 'Understand'),
            ('Develop the ability', 'Help the students develop the ability to solve problems using multivariate calculus.', 'Apply'),
            ('Multivariate calculus to other fields both within and without mathematics', 'Connect multivariate calculus to other fields both within and without mathematics.', 'Analyze'),
            ('Abstract and critical reasoning by studying proofs as applied to multivariate calculus', 'Develop abstract and critical reasoning by studying proofs as applied to multivariate calculus', 'Create'),
        ),
        'SE-357': _clos(
            ('Key concepts of Discrete Structures', 'Understand the key concepts of Discrete Structures such as Sets, Permutations, Relations, Graphs and Trees etc.', 'Understand'),
            ('Formal logic proofs and/or informal', 'Apply formal logic proofs and/or informal, but rigorous, logical reasoning to real problems, such as predicting the behavior of software or solving problems such as puzzles.', 'Apply'),
            ('Discrete structures into other computing problems', 'Apply discrete structures into other computing problems such as formal specification, verification, databases, artificial intelligence, and cryptography.', 'Apply'),
            ('Various discrete structures and their relevance within the context of computer science', 'Differentiate various discrete structures and their relevance within the context of computer science, in the areas of data structures and algorithms, in particular', 'Analyze'),
        ),
        'SE-361': _clos(
            ('History of Pakistan', 'Educate students about the history of Pakistan', 'Understand'),
            ('Various pillar of the state', 'Educate student about the various pillar of the state', 'Understand'),
            ('Government and politics', 'Educate student Government and politics', 'Understand'),
        ),
        'SE-363': _clos(
            ('Enhance the knowledge of Islam', 'Enhance the knowledge of Islam.', 'Apply'),
            ('Basic concept of Islam and Quran Pak', 'Understand the basic concept of Islam and Quran Pak.', 'Understand'),
            ('Concept of Haqooq ul ibad in the light of Quran', 'Understand the concept of Haqooq ul ibad in the light of Quran.', 'Understand'),
            ('Importance of Islamic concept about other religions', 'Know the importance of Islamic concept about other religions.', 'Remember'),
        ),
        'SE-366': _clos(
            ('Quranic verses', 'Interpret Quranic verses using various methodologies of Tafsir', 'Understand'),
            ('Implications of Quranic teachings in contemporary life', 'Discuss the implications of Quranic teachings in contemporary life', 'Understand'),
            ('Teachings of the Quran in their daily life', 'Adopt and practice the teachings of the Quran in their daily life.', 'Apply'),
        ),
        'SE-451': _clos(
            ('Various data structures and their algorithms', 'Implement various data structures and their algorithms and apply them in implementing simple applications', 'Apply'),
            ('Simple algorithms', 'Analyze simple algorithms and determine their complexities', 'Analyze'),
            ('Data structure to other application domains', 'Apply the knowledge of data structure to other application domains', 'Apply'),
            ('New data structures and algorithms', 'Design new data structures and algorithms to solve problems', 'Create'),
        ),
        'SE-452': _clos(
            ('Fundamental database concepts', 'Explain fundamental database concepts', 'Understand'),
            ('Conceptual, logical and physical database schemas', 'Design conceptual, logical and physical database schemas using different data models', 'Create'),
            ('Functional dependencies and resolve database anomalies by normalizing database tables', 'Identify functional dependencies and resolve database anomalies by normalizing database tables', 'Remember'),
            ('Structured Query Language', 'Use Structured Query Language (SQL) for database definition and manipulation in any DBMS', 'Apply'),
        ),
        'SE-453': _clos(
            ('Requirements engineering process', 'Describe the requirements engineering process', 'Understand'),
            ('Software requirements for the development of cost-effective and efficient technical solutions', 'Analyze software requirements for the development of cost-effective and efficient technical solutions.', 'Analyze'),
            ('Both functional and non-functional requirements along with validation…', 'Prepare both functional and non-functional requirements along with validation for a medium-size software system.', 'Apply'),
            ('Effective requirements in Software Requirements Specification', 'Document effective requirements in Software Requirements Specification (SRS) using clear, unambiguous requirements.', 'Create'),
        ),
        'SE-454': _clos(
            ('Role of design and its major activities within the OO…', 'Understand the role of design and its major activities within the OO software development process, with focus on the Unified process.', 'Understand'),
            ('Advantages of consistent and reliable software design', 'Comprehend the advantages of consistent and reliable software design.', 'Understand'),
            ('OOD models and refine them', 'Design OOD models and refine them to reflect implementation details', 'Create'),
            ('UML to visualize', 'Apply and use UML to visualize and document the design of software systems.', 'Apply'),
            ('Design model', 'Implement the design model using an object-oriented programming language.', 'Apply'),
        ),
        'SE-455': _clos(
            ('The concepts', 'Acquire knowledge related to the concepts, tools and techniques for the design of digital electronic circuits', 'Remember'),
            ('Demonstrate the skills to design and analyze both combinational and sequential circuits using a variety of techniques', 'Demonstrate the skills to design and analyze both combinational and sequential circuits using a variety of techniques', 'Apply'),
            ('Acquired knowledge to simulate', 'Apply the acquired knowledge to simulate and implement small-scale digital circuits', 'Apply'),
            ('Relationship between abstract logic characterizations and practical electrical implementations', 'Understand the relationship between abstract logic characterizations and practical electrical implementations', 'Understand'),
        ),
        'SE-456': _clos(
            ('Computer organization computer architecture and assembly language', 'Acquire the basic knowledge of computer organization computer architecture and assembly language', 'Remember'),
            ('Concepts of basic computer organization, architecture, and assembly language techniques', 'Understand the concepts of basic computer organization, architecture, and assembly language techniques', 'Understand'),
            ('Problems related to computer organization and assembly language', 'Solve the problems related to computer organization and assembly language', 'Apply'),
        ),
        'SE-458': _clos(
            ('Characteristics of different structures of the Operating Systems', 'Understand the characteristics of different structures of the Operating Systems and identify the core functions of the Operating Systems', 'Understand'),
            ('Algorithms of the core functions of the Operating Systems', 'Analyze and evaluate the algorithms of the core functions of the Operating Systems and explain the major performance issues with regard to the core functions', 'Analyze'),
            ('Applying system software and tools available in modern operating systems', 'Demonstrate the knowledge in applying system software and tools available in modern operating systems.', 'Apply'),
        ),
        'SE-459': _clos(
            ('Fundamental principles of communication', 'Understand the fundamental principles of communication.', 'Understand'),
            ('Effective verbal and non-verbal communication skills', 'Develop effective verbal and non-verbal communication skills.', 'Create'),
            ('Public speaking and presentation abilities', 'Enhance public speaking and presentation abilities.', 'Apply'),
            ('Techniques for professional communication', 'Learn techniques for professional communication, including emails and reports.', 'Understand'),
            ('Delivering technical presentations', 'Build confidence in delivering technical presentations.', 'Create'),
            ('Participating in group discussions, debates, and meetings', 'Improve their skills in participating in group discussions, debates, and meetings.', 'Apply'),
        ),
        'SE-460': _clos(
            ('Fundamental constructs of Python programming language', 'Understand the fundamental constructs of Python programming language', 'Understand'),
            ('Key concepts in the field of artificial intelligence', 'Understand key concepts in the field of artificial intelligence', 'Understand'),
            ('Artificial intelligence techniques and case studies', 'Implement artificial intelligence techniques and case studies', 'Apply'),
        ),
        'SE-551': _clos(
            ('Role of design and its major activities within the OO…', 'Understand the role of design and its major activities within the OO software development process, with focus on the Unified process', 'Understand'),
            ('Object-oriented design models and refine them', 'Develop Object-oriented design models and refine them to reflect implementation details', 'Create'),
            ('Different architectures for a medium size software', 'Evaluate different architectures for a medium size software.', 'Evaluate'),
            ('Design model', 'Implement design model using an object-oriented programming language.', 'Apply'),
        ),
        'SE-552': _clos(
            ('What is meant by “best”', 'Explain what is meant by “best”, “expected”, and “worst” case behavior of an algorithm', 'Understand'),
            ('Characteristics of data and/or other conditions or assumptions…', 'Identify the characteristics of data and/or other conditions or assumptions that lead to different behaviors.', 'Remember'),
            ('Informally the time and space complexity of simple algorithms', 'Determine informally the time and space complexity of simple algorithms', 'Analyze'),
            ('Standard complexity classes', 'List and contrast standard complexity classes', 'Remember'),
            ('Big O', 'Use big O, Omega, Theta notation formally to give asymptotic upper bounds on time and space complexity of algorithms', 'Apply'),
            ('Of the strategies', 'Use of the strategies (brute-force, greedy, divide-and- conquer, and dynamic programming) to solve an appropriate problem', 'Apply'),
            ('Solve problems using graph algorithms, including single- source and all-pairs shortest paths, and at least one minimum spanning tree algorithm', 'Solve problems using graph algorithms, including single- source and all-pairs shortest paths, and at least one minimum spanning tree algorithm', 'Apply'),
            ('And/or implement a string-matching algorithm', 'Trace and/or implement a string-matching algorithm', 'Analyze'),
        ),
        'SE-553': _clos(
            ('Principles of the project lifecycle and how', 'Explain principles of the project lifecycle and how to identify opportunities to work with learners on relevant and appropriate project scenarios to share this understanding', 'Understand'),
            ('Issues around project management and its application in the real…', 'Evaluate and discuss the issues around project management and its application in the real world with course participants and learners.', 'Evaluate'),
            ('Project management techniques for IT projects to initiate, plan, execute', 'Choose project management techniques for IT projects to initiate, plan, execute and evaluate a project and work in teams to create a project plan for a project scenario that includes key tasks, critical path, dependencies and a realistic timeline.', 'Evaluate'),
            ('Strategies for gaining confidence in managing projects', 'Present strategies for gaining confidence in managing projects through simple project planning examples.', 'Apply'),
        ),
        'SE-554': _clos(
            ('Software testing and software quality assurance principles', 'Outline software testing and software quality assurance principles.', 'Understand'),
            ('Test case', 'Prepare test case and test suites for completely testing all aspects of a system under test (SUT)', 'Apply'),
            ('Which of the software testing techniques are relevant for a particular case', 'Analyze which of the software testing techniques are relevant for a particular case and know software reliability analysis tools and techniques.', 'Analyze'),
            ('Findings of a quality assurance cycle', 'Compile findings of a quality assurance cycle.', 'Create'),
        ),
        'SE-555': _clos(
            ('Key terminologies and technologies of computer networks', 'Describe the key terminologies and technologies of computer networks', 'Understand'),
            ('Services and functions provided by each layer in the Internet protocol stack', 'Explain the services and functions provided by each layer in the Internet protocol stack', 'Understand'),
            ('Various internetworking devices and protocols and their functions in a networking', 'Identify various internetworking devices and protocols and their functions in a networking', 'Remember'),
            ('Working and performance of key technologies, algorithms and protocols', 'Analyze working and performance of key technologies, algorithms and protocols', 'Analyze'),
        ),
        'SE-556': _clos(
            ('Key concepts of information security', 'Explain key concepts of information security such as design principles, cryptography, risk management, and ethics', 'Understand'),
            ('Legal, ethical, and professional issues in information security', 'Discuss legal, ethical, and professional issues in information security', 'Understand'),
            ('Various security and risk management tools for achieving information security and privacy', 'Apply various security and risk management tools for achieving information security and privacy', 'Apply'),
            ('Appropriate techniques to tackle', 'Identify appropriate techniques to tackle and solve problems in the discipline of information security', 'Remember'),
        ),
        'SE-557': _clos(
            ('Different concepts in automata theory and formal languages', 'Explain and manipulate the different concepts in automata theory and formal languages such as formal proofs, automata, regular expressions, Turing machines etc.', 'Understand'),
            ('Properties of languages', 'Prove properties of languages, grammars and automata with rigorously formal mathematical methods', 'Evaluate'),
            ('Of automata, RE and CFG', 'Design of automata, RE and CFG', 'Create'),
            ('Between equivalent NFAs, DFAs and Res', 'Transform between equivalent NFAs, DFAs and Res', 'Apply'),
            ('Turing machines performing simple tasks', 'Define Turing machines performing simple tasks', 'Remember'),
            ('Formal descriptions of languages', 'Differentiate and manipulate formal descriptions of languages, automata and grammars with focus on regular and context-free languages, finite automata and regular expressions.', 'Analyze'),
        ),
        'SE-572': _clos(
            ('Advance data models', 'Understanding advance data models, technologies and approaches for building distributed database systems.', 'Understand'),
            ('Models and approaches', 'Applying the models and approaches in order to become enabled to select and apply appropriate methods for a particular case', 'Apply'),
            ('Database solution for a given scenario/ challenging problem…', 'Develop a database solution for a given scenario/ challenging problem in the domain of distributed database systems.', 'Create'),
        ),
        'SE-575': _clos(
            ('Different architectures & framework for Mobile Application development', 'Discuss different architectures & framework for Mobile Application development.', 'Understand'),
            ('Mobile applications', 'Develop mobile applications using current software development environments.', 'Create'),
            ('Different performance tradeoffs in mobile application development', 'Compare the different performance tradeoffs in mobile application development.', 'Analyze'),
        ),
        'SE-652': _clos(
            ('About parallel and distributed computers', 'Learn about parallel and distributed computers.', 'Understand'),
            ('Portable programs for parallel or distributed-architectures', 'Write portable programs for parallel or distributed-architectures using Message-Passing Interface (MPI) Library', 'Apply'),
            ('Complex problems with shared memory-programming with openMP', 'Analyze complex problems with shared memory-programming with openMP', 'Analyze'),
        ),
        'SE-671': _clos(
            ('Concepts and technique of software re- engineering', 'Explain the concepts and technique of software re- engineering.', 'Understand'),
            ('Reengineering techniques to maintain and modify software systems', 'Apply reengineering techniques to maintain and modify software systems', 'Apply'),
            ('Maintenance related problems associated with object-oriented software systems', 'Analyze and understand maintenance related problems associated with object-oriented software systems.', 'Analyze'),
            ('Complex design reengineering and reverse engineering problems', 'Perform complex design reengineering and reverse engineering problems.', 'Apply'),
        ),
        'SE-677': _clos(
            ('How web standards impact software development', 'Discuss how web standards impact software development.', 'Understand'),
            ('Constraints that the web puts on developers', 'Describe the constraints that the web puts on developers.', 'Understand'),
            ('Simple web application', 'Design and implement a simple web application.', 'Create'),
            ('Existing web application against a current web standard', 'Review an existing web application against a current web standard.', 'Understand'),
        ),
    },
    'BSAI': {
        'AI-351': _clos(
            ('Problem-solving and logic constructs', 'Understand problem-solving and logic constructs', 'Understand'),
            ('Programing concepts', 'Implement programing concepts', 'Apply'),
            ('Design and implement algorithms to solve real world problems', 'Design and implement algorithms to solve real world problems', 'Create'),
        ),
        'AI-352': _clos(
            ('Principles of object-oriented paradigm', 'Understand principles of object-oriented paradigm.', 'Understand'),
            ('Objects and their relationships', 'Identify the objects and their relationships to build object-oriented solution', 'Remember'),
            ('Solution for a given problem', 'Model a solution for a given problem using object-oriented principles', 'Create'),
            ('Object-oriented solution', 'Examine an object-oriented solution', 'Analyze'),
        ),
        'AI-353': _clos(
            ('Basics of computing technology', 'Understand basics of computing technology', 'Understand'),
            ('Number systems conversions and arithmetic', 'Do number systems conversions and arithmetic', 'Apply'),
            ('Types of software', 'Have knowledge of types of software', 'Remember'),
            ('Computing related technologies', 'Have knowledge of computing related technologies', 'Remember'),
        ),
        'AI-354': _clos(
            ('Acquire knowledge related to concepts, tools and techniques for the design of digital electronic circuits', 'Acquire knowledge related to concepts, tools and techniques for the design of digital electronic circuits', 'Remember'),
            ('Demonstrate the skills to design and analyze both combinational and sequential circuits using a variety of techniques', 'Demonstrate the skills to design and analyze both combinational and sequential circuits using a variety of techniques', 'Apply'),
            ('Acquired knowledge to simulate', 'Apply the acquired knowledge to simulate and implement small-scale digital circuits', 'Apply'),
            ('Relationship between abstract logic characterizations and practical electrical implementations', 'Understand the relationship between abstract logic characterizations and practical electrical implementations', 'Understand'),
        ),
        'AI-355': _clos(
            ('Fundamental concepts of differential and integral calculus', 'Understand the fundamental concepts of differential and integral calculus.', 'Understand'),
            ('Apply calculus to solve problems in optimization, curve sketching, and area calculation', 'Apply calculus to solve problems in optimization, curve sketching, and area calculation.', 'Apply'),
            ('Conic sections', 'Analyze and interpret conic sections using analytical geometry.', 'Analyze'),
            ('Calculus concepts in AI applications', 'Utilize calculus concepts in AI applications such as machine learning algorithms, neural networks, and robotics.', 'Apply'),
            ('Problem-solving skills relevant to AI technologies', 'Develop problem-solving skills relevant to AI technologies through mathematical modeling.', 'Create'),
        ),
        'AI-356': _clos(
            ('Vector and matrix operations', 'Understand and manipulate vector and matrix operations.', 'Understand'),
            ('Systems of linear equations', 'Solve systems of linear equations using various methods.', 'Apply'),
            ('Concepts of vector spaces, subspaces, bases, and dimensions', 'Grasp the concepts of vector spaces, subspaces, bases, and dimensions.', 'Understand'),
            ('Eigenvalues and eigenvectors in practical scenarios', 'Apply eigenvalues and eigenvectors in practical scenarios, especially in AI and machine learning models.', 'Apply'),
            ('Linear transformations', 'Use linear transformations to model real-world problems in AI.', 'Apply'),
            ('Linear algebra operations', 'Implement linear algebra operations using computational tools such as Python and MATLAB.', 'Apply'),
        ),
        'AI-357': _clos(
            ('Core physics principles to real-world problems', 'Apply core physics principles to real-world problems and conduct experiments that demonstrate these concepts', 'Apply'),
            ('Analytical skills and effectively communicate scientific ideas', 'Enhance your analytical skills and effectively communicate scientific ideas.', 'Apply'),
        ),
        'AI-358': _clos(
            ('Key concepts of Discrete Structures', 'Understand the key concepts of Discrete Structures such as Sets, Permutations, Relations, Graphs and Trees etc.', 'Understand'),
            ('Formal logic proofs and/or informal', 'Apply formal logic proofs and/or informal, but rigorous, logical reasoning to real problems, such as predicting the behavior of software or solving problems such as puzzles.', 'Apply'),
            ('Discrete structures into other computing problems', 'Apply discrete structures into other computing problems such as formal specification, verification, databases, artificial intelligence, and cryptography.', 'Apply'),
            ('Various discrete structures and their relevance within the context of computer science', 'Differentiate various discrete structures and their relevance within the context of computer science, in the areas of data structures and algorithms, in particular', 'Analyze'),
        ),
        'AI-359': _clos(
            ('Understanding and application of English grammar', 'Enhance their understanding and application of English grammar.', 'Apply'),
            ('Strong vocabulary relevant to academic and professional use', 'Develop a strong vocabulary relevant to academic and professional use.', 'Create'),
            ('Reading comprehension and critical analysis of texts', 'Improve their reading comprehension and critical analysis of texts.', 'Apply'),
            ('Writing skills, focusing on academic and technical writing', 'Strengthen their writing skills, focusing on academic and technical writing.', 'Apply'),
            ('Oral communication', 'Gain confidence in oral communication, including presentations and discussions.', 'Understand'),
            ('Techniques for effective communication in professional environments', 'Learn techniques for effective communication in professional environments.', 'Understand'),
            ('Academic and technical reports', 'Writing academic and technical reports.', 'Create'),
        ),
        'AI-360': _clos(
            ('Fundamental principles of communication', 'Understand the fundamental principles of communication.', 'Understand'),
            ('Effective verbal and non-verbal communication skills', 'Develop effective verbal and non-verbal communication skills.', 'Create'),
            ('Public speaking and presentation abilities', 'Enhance public speaking and presentation abilities.', 'Apply'),
            ('Techniques for professional communication', 'Learn techniques for professional communication, including emails and reports.', 'Understand'),
            ('Delivering technical presentations', 'Build confidence in delivering technical presentations.', 'Create'),
            ('Participating in group discussions, debates, and meetings', 'Improve their skills in participating in group discussions, debates, and meetings.', 'Apply'),
        ),
        'AI-361': _clos(
            ('Enhance the knowledge of Islam', 'Enhance the knowledge of Islam.', 'Apply'),
            ('Basic concept of Islam and Quran Pak', 'Understand the basic concept of Islam and Quran Pak.', 'Understand'),
            ('Concept of Haqooq ul ibad in the light of Quran', 'Understand the concept of Haqooq ul ibad in the light of Quran.', 'Understand'),
            ('Importance of Islamic concept about other religions', 'Know the importance of Islamic concept about other religions.', 'Remember'),
        ),
        'AI-362': _clos(
            ('History of Pakistan', 'Educate students about the history of Pakistan', 'Understand'),
            ('Various pillar of the state', 'Educate students about the various pillar of the state', 'Understand'),
            ('Government and politics', 'Educate student Government and politics', 'Understand'),
        ),
        'AI-444': _clos(
            ('Quranic verses', 'Interpret Quranic verses using various methodologies of Tafsir', 'Understand'),
            ('Implications of Quranic teachings in contemporary life', 'Discuss the implications of Quranic teachings in contemporary life', 'Understand'),
            ('Teachings of the Quran in their daily life', 'Adopt and practice the teachings of the Quran in their daily life.', 'Apply'),
        ),
        'AI-451': _clos(
            ('Various data structures and their algorithms', 'Implement various data structures and their algorithms and apply them in implementing simple applications', 'Apply'),
            ('Simple algorithms', 'Analyze simple algorithms and determine their complexities', 'Analyze'),
            ('Data structure to other application domains', 'Apply the knowledge of data structure to other application domains', 'Apply'),
            ('New data structures and algorithms', 'Design new data structures and algorithms to solve problems', 'Create'),
        ),
        'AI-452': _clos(
            ('Fundamental database concepts', 'Explain fundamental database concepts', 'Understand'),
            ('Conceptual, logical and physical database schemas', 'Design conceptual, logical and physical database schemas using different data models', 'Create'),
            ('Functional dependencies and resolve database anomalies by normalizing database tables', 'Identify functional dependencies and resolve database anomalies by normalizing database tables', 'Remember'),
            ('Structured Query Language', 'Use Structured Query Language (SQL) for database definition and manipulation in any DBMS', 'Apply'),
        ),
        'AI-453': _clos(
            ('Various software engineering processes and activates', 'Describe various software engineering processes and activates', 'Understand'),
            ('System modeling techniques', 'Apply the system modeling techniques to model a medium size software system', 'Apply'),
            ('Software quality assurance and testing principles to medium size software systems', 'Apply software quality assurance and testing principles to medium size software systems', 'Apply'),
            ('Key principles and common methods for software project management', 'Discuss key principles and common methods for software project management such as scheduling, size estimation, cost estimation and risk analysis Course Objectives The goal of software engineering course applies a disciplined and organized approach to software development with the stated goal of improving quality, time and budget efficiency, along with the assurance of structured testing and engineer Certification.', 'Understand'),
        ),
        'AI-454': _clos(
            ('Fundamental constructs of programming languages used for AI', 'Understand the fundamental constructs of programming languages used for AI', 'Understand'),
            ('Key concepts in the field of artificial intelligence', 'Understand key concepts in the field of artificial intelligence', 'Understand'),
            ('Artificial intelligence techniques and case studies', 'Implement artificial intelligence techniques and case studies', 'Apply'),
        ),
        'AI-455': _clos(
            ('Computer organization computer architecture and assembly language', 'Acquire the basic knowledge of computer organization computer architecture and assembly language', 'Remember'),
            ('Concepts of basic computer organization, architecture, and assembly language techniques', 'Understand the concepts of basic computer organization, architecture, and assembly language techniques', 'Understand'),
            ('Problems related to computer organization and assembly language', 'Solve the problems related to computer organization and assembly language', 'Apply'),
        ),
        'AI-456': _clos(
            ('Key terminologies and technologies of computer networks', 'Describe the key terminologies and technologies of computer networks', 'Understand'),
            ('Services and functions provided by each layer in the Internet protocol stack', 'Explain the services and functions provided by each layer in the Internet protocol stack', 'Understand'),
            ('Various internetworking devices and protocols and their functions in a networking', 'Identify various internetworking devices and protocols and their functions in a networking', 'Remember'),
            ('Working and performance of key technologies, algorithms and protocols', 'Analyze working and performance of key technologies, algorithms and protocols', 'Analyze'),
        ),
        'AI-459': _clos(
            ('Basic principles of probability theory', 'Understand and apply the basic principles of probability theory.', 'Understand'),
            ('Analyze data using statistical methods and draw valid conclusions', 'Analyze data using statistical methods and draw valid conclusions.', 'Analyze'),
            ('Probability models', 'Use probability models to describe random processes and uncertainty.', 'Apply'),
            ('Statistical techniques in AI and machine learning problems', 'Apply statistical techniques in AI and machine learning problems.', 'Apply'),
            ('Software tools for statistical analysis and data visualization', 'Use software tools for statistical analysis and data visualization.', 'Apply'),
        ),
        'AI-471': _clos(
            ('Different concepts in automata theory and formal languages', 'Explain and manipulate the different concepts in automata theory and formal languages such as formal proofs, automata, regular expressions, Turing machines etc.', 'Understand'),
            ('Properties of languages', 'Prove properties of languages, grammars and automata with rigorously formal mathematical methods', 'Evaluate'),
            ('Of automata, RE and CFG', 'Design of automata, RE and CFG', 'Create'),
            ('Between equivalent NFAs, DFAs and Res', 'Transform between equivalent NFAs, DFAs and Res', 'Apply'),
            ('Turing machines performing simple tasks', 'Define Turing machines performing simple tasks', 'Remember'),
            ('Formal descriptions of languages', 'Differentiate and manipulate formal descriptions of languages, automata and grammars with focus on regular and context-free languages, finite automata and regular expressions. 7.', 'Analyze'),
        ),
        'AI-472': _clos(
            ('Fundamental concepts of Scientific Programming', 'Understand the fundamental concepts of Scientific Programming using programing Language(s)', 'Understand'),
            ('Computer algebra system', 'Use a computer algebra system to investigate and solve mathematical problems relating to integration, differential equations and approximation', 'Apply'),
        ),
        'AI-553': _clos(
            ('Characteristics of different structures of the Operating Systems', 'Understand the characteristics of different structures of the Operating Systems and identify the core functions of the Operating Systems', 'Understand'),
            ('Algorithms of the core functions of the Operating Systems', 'Analyze and evaluate the algorithms of the core functions of the Operating Systems and explain the major performance issues with regard to the core functions', 'Analyze'),
            ('Applying system software and tools available in modern operating systems', 'Demonstrate the knowledge in applying system software and tools available in modern operating systems.', 'Apply'),
        ),
        'AI-554': _clos(
            ('Key skills in ethical decision-making and effective communication in a professional environment', 'Develop key skills in ethical decision-making and effective communication in a professional environment', 'Create'),
            ('Navigate workplace dynamics', 'Learn how to navigate workplace dynamics and enhance your collaboration and leadership abilities.', 'Understand'),
        ),
        'AI-556': _clos(
            ('What is meant by “best”', 'Explain what is meant by “best”, “expected”, and “worst” case behavior of an algorithm', 'Understand'),
            ('Characteristics of data and/or other conditions or assumptions…', 'Identify the characteristics of data and/or other conditions or assumptions that lead to different behaviors.', 'Remember'),
            ('Informally the time and space complexity of simple algorithms', 'Determine informally the time and space complexity of simple algorithms', 'Analyze'),
            ('Standard complexity classes', 'List and contrast standard complexity classes', 'Remember'),
            ('Big O', 'Use big O, Omega, Theta notation formally to give asymptotic upper bounds on time and space complexity of algorithms', 'Apply'),
            ('Of the strategies', 'Use of the strategies (brute-force, greedy, divide-and- conquer, and dynamic programming) to solve an appropriate problem', 'Apply'),
            ('Solve problems using graph algorithms, including single- source and all-pairs shortest paths, and at least one minimum spanning tree algorithm', 'Solve problems using graph algorithms, including single- source and all-pairs shortest paths, and at least one minimum spanning tree algorithm', 'Apply'),
            ('And/or implement a string-matching algorithm', 'Trace and/or implement a string-matching algorithm', 'Analyze'),
        ),
        'AI-557': _clos(
            ('Key concepts of information security', 'Explain key concepts of information security such as design principles, cryptography, risk management, and ethics', 'Understand'),
            ('Legal, ethical, and professional issues in information security', 'Discuss legal, ethical, and professional issues in information security', 'Understand'),
            ('Various security and risk management tools for achieving information security and privacy', 'Apply various security and risk management tools for achieving information security and privacy', 'Apply'),
            ('Appropriate techniques to tackle', 'Identify appropriate techniques to tackle and solve problems in the discipline of information security', 'Remember'),
        ),
        'AI-559': _clos(
            ('Civic Responsibilities', 'Understand Civic Responsibilities: Explain the principles of civic duty, community involvement, and the roles of government and individuals in society.', 'Understand'),
            ('Social Issues', 'Analyze Social Issues: Identify and analyze pressing social, political, and economic issues within local, national, and global contexts, understanding their impact on communities.', 'Analyze'),
            ('Community-Based Learning', 'Engage in Community-Based Learning: Participate in activities that foster community engagement, applying course concepts to real-world scenarios through volunteer work, community projects, or partnerships.', 'Apply'),
            ('Critical Thinking on Public Policy', 'Develop Critical Thinking on Public Policy: Evaluate public policies and proposals, considering their implications for social justice, equity, and community well-being.', 'Create'),
            ('Effective Communication and Advocacy', 'Practice Effective Communication and Advocacy: Demonstrate skills in communicating ideas, advocating for community needs, and engaging with diverse audiences through written, oral, and digital means.', 'Apply'),
            ('Personal and Social Impact', 'Reflect on Personal and Social Impact: Assess personal values and actions in relation to civic responsibilities, exploring how individual contributions can promote positive social change.', 'Evaluate'),
            ('Community Solutions', 'Collaborate for Community Solutions: Work collaboratively on community-based projects, developing strategies to address social issues and strengthen community resilience.', 'Apply'),
        ),
        'AI-576': _clos(
            ('Different architectures & framework for Mobile Application development', 'Discuss different architectures & framework for Mobile Application development.', 'Understand'),
            ('Mobile applications', 'Develop mobile applications using current software development environments.', 'Create'),
            ('Different performance tradeoffs in mobile application development', 'Compare the different performance tradeoffs in mobile application development.', 'Analyze'),
        ),
        'AI-578': _clos(
            ('Architecture and core components of IoT systems', 'Understand the architecture and core components of IoT systems.', 'Understand'),
            ('Various IoT communication protocols and networking techniques', 'Learn various IoT communication protocols and networking techniques.', 'Understand'),
            ('AI techniques for data collection', 'Apply AI techniques for data collection, processing, and decision-making in IoT environments.', 'Apply'),
            ('Security, privacy, and ethical implications of IoT systems', 'Explore the security, privacy, and ethical implications of IoT systems.', 'Analyze'),
            ('Hands-on experience in IoT device programming and deployment', 'Develop hands-on experience in IoT device programming and deployment.', 'Create'),
        ),
        'AI-652': _clos(
            ('About parallel and distributed computers', 'Learn about parallel and distributed computers.', 'Understand'),
            ('Portable programs for parallel or distributed-architectures', 'Write portable programs for parallel or distributed-architectures using Message-Passing Interface (MPI) Library', 'Apply'),
            ('Complex problems with shared memory-programming with openMP', 'Analyze complex problems with shared memory-programming with openMP', 'Analyze'),
        ),
        'AI-657': _clos(
            ('Fundamental constructs of Lisp, Prolog, and Python programming languages', 'Understand the fundamental constructs of Lisp, Prolog, and Python programming languages', 'Understand'),
            ('Fundamental constructs of programming languages for data analysis and representation', 'Comprehend the fundamental constructs of programming languages for data analysis and representation', 'Understand'),
            ('Object-oriented concepts in the programming languages', 'Understand and apply the Object-oriented concepts in the programming languages', 'Understand'),
            ('Various libraries for plotting, interpreting and analyzing data in Python', 'Apply various libraries for plotting, interpreting and analyzing data in Python', 'Apply'),
        ),
        'AI-675': _clos(
            ('Fundamental concepts and challenges in cyber security', 'Understand fundamental concepts and challenges in cyber security.', 'Understand'),
            ('Different types of cyber threats, vulnerabilities, and attack vectors', 'Explore different types of cyber threats, vulnerabilities, and attack vectors.', 'Analyze'),
            ('Basic cryptographic techniques and security protocols', 'Implement basic cryptographic techniques and security protocols.', 'Apply'),
            ('AI techniques', 'Apply AI techniques to enhance cyber security measures, such as intrusion detection systems.', 'Apply'),
            ('Case studies of cyber-attacks', 'Analyze case studies of cyber-attacks and devise mitigation strategies.', 'Analyze'),
            ('Ethical and legal concerns in cyber security', 'Understand ethical and legal concerns in cyber security.', 'Understand'),
        ),
        'AI-676': _clos(
            ('How web standards impact software development', 'Discuss how web standards impact software development.', 'Understand'),
            ('Constraints that the web puts on developers', 'Describe the constraints that the web puts on developers.', 'Understand'),
            ('Simple web application', 'Design and implement a simple web application.', 'Create'),
            ('Existing web application against a current web standard', 'Review an existing web application against a current web standard.', 'Understand'),
        ),
        'AI-677': _clos(
            ('Biological foundations necessary for bioinformatics', 'Understand the biological foundations necessary for bioinformatics.', 'Understand'),
            ('DNA, RNA, and protein sequences', 'Analyze DNA, RNA, and protein sequences using computational tools.', 'Analyze'),
            ('Algorithms and AI techniques for biological data analysis', 'Apply algorithms and AI techniques for biological data analysis.', 'Apply'),
            ('Bioinformatics databases', 'Explore bioinformatics databases and understand their use in research.', 'Analyze'),
            ('Machine learning for predicting biological structures and functions', 'Use machine learning for predicting biological structures and functions.', 'Apply'),
            ('Real-world problems in genomics, proteomics, and other biological domains', 'Solve real-world problems in genomics, proteomics, and other biological domains.', 'Apply'),
        ),
        'AI-678': _clos(
            ('Key Concepts', 'Understand Key Concepts: Explain fundamental concepts in complex networks, including graph theory, nodes, edges, and network topology.', 'Understand'),
            ('Network Structures', 'Analyze Network Structures: Analyze various types of networks, such as social, biological, and technological networks, and identify their structural properties.', 'Analyze'),
            ('Complex Systems', 'Model Complex Systems: Develop and apply mathematical models to simulate the behavior of complex networks.', 'Create'),
            ('Network Dynamics', 'Identify Network Dynamics: Explore the dynamics of network evolution, including growth patterns, clustering, and community detection.', 'Remember'),
            ('Network Resilience', 'Evaluate Network Resilience: Assess the robustness and vulnerability of networks to failures and attacks.', 'Evaluate'),
        ),
    },
}
