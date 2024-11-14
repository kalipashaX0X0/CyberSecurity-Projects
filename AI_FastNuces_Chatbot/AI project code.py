




# Author: Fahad Yaseen
# Institution: FAST NUCES
# Project: AI Chatbot Development







import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Sample data and responses
data = [
    "What is the application deadline for the university?",
    "What is the tuition fee for international students?",
    "How do I apply for financial aid?",
    "What are the requirements for admission?",
    "What is the contact information for the admissions office?",
    "What are the admission requirements?",
    "How do I apply to the university?",
    "When is the application deadline?",
    "What programs do you offer?",
    "How much is tuition?",
    "What financial aid options are available?",
    "Can I schedule a campus tour?",
    "What is the student-to-faculty ratio?",
    "How do I contact an academic advisor?",
    "What is the campus safety record?",
    "Are there any on-campus housing options?",
    "What extracurricular activities are available?",
    "What is the graduation rate?",
    "Are there any internships or co-op programs available?",
    "What is the average class size?",
    "What are the minimum GPA and test score requirements?",
    "Can I transfer credits from another institution?",
    "What is the academic calendar?",
    "How do I access the library resources?",
    "What is the campus culture like?",
    "Are there any study abroad programs?",
    "What is the acceptance rate?",
    "How do I change my major?",
    "Is there a career services center on campus?",
    "What are the academic support services available?",
    "How do I apply for scholarships?",
    "What is the faculty's background and experience?",
    "Are there any research opportunities for students?",
    "How do I register for classes?",
    "What is the curriculum like for my major?",
    "Can I take courses from other departments or schools?",
    "How do I access online courses",
    "What is the grading system?",
    "Are there any prerequisites for my major?",
    "What is the attendance policy?",
    "How do I appeal a grade?",
    "Are there any tutoring services available?",
    "How do I access disability services?",
    "What is the process for academic probation or suspension?",
    "What is the university's mission statement?",
    "How is the university addressing diversity and inclusion?",
    "How do I access the campus health services?",
    "What is the athletic program like?",
    "How do I purchase textbooks?",
    "Are there any language or culture exchange programs available?",
    "How do I access the student portal?",
    "What is the policy for dropping or adding courses?",
    "How do I access student organizations?",
    "What is the policy on academic dishonesty?",
    "Are there any career fairs or networking events on campus?"
]

responses = [
    "The application deadline is June 1st.",
    "The tuition fee for international students is $30,000 per year.",
    "You can apply for financial aid by filling out the FAFSA form.",
    "The requirements for admission include a high school diploma, transcripts, and SAT or ACT scores. You can find the full list on our website.",
    "You can contact the admissions office at admissions@university.edu or by calling 555-1234.",
    "You can find the admission requirements on our website under the admissions tab.",
    "You can apply to the university online through our website.",
    "The application deadline is March 1st.",
    "We offer a variety of programs. You can find a list of them on our website.",
    "Tuition fees vary depending on the program. You can find the exact cost on our website.",
    "We offer various financial aid options such as scholarships, grants, and loans. You can find more information on our website or by contacting our financial aid office.",
    "Yes, you can schedule a campus tour through our website or by contacting our admissions office.",
    "Our student-to-faculty ratio is 18:1.",
    "You can contact your academic advisor through our website or by visiting the academic advising office on campus.",
    "Our campus has a strong safety record, with 24-hour security and surveillance systems in place. You can find more information about campus safety on our website.",
    "Yes, we have several on-campus housing options available for students. You can find more information about them on our website.",
    "We offer a wide range of extracurricular activities, including sports teams, clubs, and organizations. You can find more information about them on our website.",
    "Our graduation rate varies by program, but overall it is around 85%. You can find more specific information about graduation rates on our website.",
    "Yes, we have several internship and co-op programs available for students. You can find more information about them on our website or by contacting our career services office.",
    "Our average class size is around 20 students.",
    "The minimum GPA and test score requirements vary by program. You can find more information about them on our website.",
    "Yes, you can transfer credits from another institution. You will need to provide official transcripts and meet certain requirements. You can find more information about the transfer process on our website.",
    "Our academic calendar can be found on our website. It includes important dates such as the start and end of semesters, holidays, and exam periods.",
    "You can access the library resources by visiting our library on campus or by accessing them online through our website. You will need to have a valid student ID to check out physical materials.",
    "Our campus has a diverse and inclusive culture, with a strong focus on academic excellence and community involvement. We have a variety of events and activities throughout the year to foster a sense of community and engagement among students.",
    "Yes, we offer study abroad programs. You can find more information on our website or by speaking with an academic advisor.",
    "The acceptance rate varies by program and year. You can find more information on our website or by speaking with an admissions counselor.",
    "You can change your major by speaking with an academic advisor and filling out the necessary paperwork.",
    "Yes, there is a career services center on campus. You can find more information on our website or by visiting the center in person.",
    "We offer a variety of academic support services, including tutoring, study groups, and academic advising. You can find more information on our website or by speaking with an academic advisor.",
    "You can apply for scholarships by filling out the necessary forms and submitting them to the financial aid office. You can find more information on our website or by speaking with a financial aid counselor.",
    "Our faculty comes from a diverse range of backgrounds and experiences. You can find more information about individual faculty members on our website or by speaking with an academic advisor.",
    "Yes, there are research opportunities available for students. You can find more information on our website or by speaking with a faculty member or academic advisor.",
    "You can register for classes online through our student portal. You can find more information on our website or by speaking with an academic advisor.",
    "The curriculum for each major varies, but you can find more information on our website or by speaking with an academic advisor.",
    "Yes, you can take courses from other departments or schools. However, you will need to meet certain requirements and obtain permission from your academic advisor and the department offering the course.",
    "You can access online courses through our university's learning management system. Once you log in, you will be able to view your courses and access course materials.",
    "We use a letter grading system with grades ranging from A to F. The specific grading criteria and scale may vary depending on the course and instructor.",
    "Yes, there are prerequisites for certain majors. You can find the specific requirements for your major in the university's course catalog or by speaking with your academic advisor.",
    "Attendance policies may vary by course and instructor. You should refer to your course syllabus for specific attendance requirements.",
    "You can appeal a grade by following the university's grade appeal process. This typically involves submitting a formal written appeal to the department offering the course.",
    "Yes, the university offers tutoring services to help students with their coursework. You can find information about tutoring services on the university's website or by speaking with your academic advisor.",
    "To access disability services, you will need to register with the university's office of disability services. They can provide you with accommodations and support to help you succeed in your coursework.",
    "The process for academic probation or suspension can vary depending on the specific circumstances. Generally, you will be placed on academic probation if your GPA falls below a certain level. If you do not improve your grades during the probationary period, you may be subject to suspension.",
    "Our university's mission is to provide a comprehensive education that prepares students for success in their chosen fields, promotes intellectual curiosity and lifelong learning, and fosters a sense of civic responsibility and global awareness.",
    "Our university values diversity and inclusivity and has several initiatives in place to address these issues. These include programs such as diversity and inclusion training for faculty and staff, the establishment of resource centers for underrepresented students, and the creation of student-led organizations dedicated to promoting diversity and inclusion on campus.",
    "Our campus health services are easily accessible to all students. You can schedule an appointment with a healthcare provider online or by calling the health center directly. Walk-in appointments are also available for urgent medical needs. We offer a wide range of medical services, including primary care, women's health, mental health, and dental care.",
    "Our university has a thriving athletic program with numerous sports teams for both men and women. Our teams compete at the Division I level and have a strong record of success in various sports. We also offer numerous recreational sports programs for students who want to stay active and engage in physical activity.",
    "You can purchase textbooks for your courses through our campus bookstore or online through our website. We offer new and used textbooks, as well as digital versions of many texts. We also have a textbook rental program for students who prefer to rent rather than purchase.",
    "Yes, we offer a variety of language and culture exchange programs for students who are interested in learning about other cultures and languages. These programs include study abroad opportunities, language immersion programs, and international student exchange programs.",
    "Our student portal is easily accessible online through our university website. Once you log in, you can access your course schedule, grades, financial aid information, and other important student resources.",
    "Students can drop or add courses during the first few weeks of the semester without penalty. After that, there may be deadlines and fees associated with dropping or adding courses. It's important to check with your academic advisor or registrar's office for specific information about the policy and deadlines.",
    "We have a wide range of student organizations available for students to join, including academic, cultural, social, and recreational groups. You can access information about these organizations through our student portal or by attending student organization fairs and events.",
    "Our university takes academic dishonesty very seriously and has strict policies in place to prevent and address such behavior. Academic dishonesty includes plagiarism, cheating, and other forms of misconduct. Penalties for academic dishonesty can range from a failing grade on an assignment to expulsion from the university.",
    "Yes, we hold career fairs and networking events on campus throughout the year to connect students with potential employers and help them explore career opportunities. We also offer career counseling and resume-building workshops to help students prepare for their job search."
    
    
    
        
]
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
vectorizer = TfidfVectorizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(tokens)

corpus = [preprocess(text) for text in data]
tfidf = vectorizer.fit_transform(corpus)

def generate_response(query):
    query_tfidf = vectorizer.transform([preprocess(query)])
    cosine_similarities = cosine_similarity(query_tfidf, tfidf).flatten()
    n = 3
    indices = cosine_similarities.argsort()[::-1][:n]
    threshold = 0.5
    if cosine_similarities[indices[0]] >= threshold:
        return responses[indices[0]]
    else:
        return "I'm sorry, I didn't understand your question. Can you please rephrase it?"
def chatbot():
    print("----------------------------------------------------------------------------------------------")
    print("\nWelcome to the Fast Student Service Chatbot\n"
    " \n\nHow can I assist you today? (type 'quit' to exit)\n")
    print("----------------------------------------------------------------------------------------------")
    while True:
        query = input("You: ")
        if query.lower() == "quit":
            print("Thank You ! If you have any more questions, feel free to ask... "
                "\n What about my Weightage ? ")
            break
        response = generate_response(query)
        print("OneStop: " + response)
chatbot()
