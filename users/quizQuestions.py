from app import db
from models import Question, Quiz


def cookingTerminology1():
    new_quiz1 = Quiz(quizName="Test Quiz 1", quizDescription="Introduction to Peppers", order=1)

    db.session.add(new_quiz1)
    db.session.commit()

    question1 = Question(
        quizID=new_quiz1.quizID,
        questionText="What color are bell peppers?",
        correctAnswer="Green, Red, Yellow, and Orange",
        otherOptions=["Blue", "Purple", "Black"]
    )

    question2 = Question(
        quizID=new_quiz1.quizID,
        questionText="Which pepper is the spiciest?",
        correctAnswer="Carolina Reaper",
        otherOptions=["Jalapeno", "Bell Pepper", "Banana Pepper"]
    )

    db.session.add(question1)
    db.session.add(question2)
