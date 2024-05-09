from app import db
from models import Question, Quiz


def easy_quiz():
    easyQuiz = Quiz(quizName="Easy Quiz: Vegan Basics", quizDescription="An introductory quiz on general and basic "
                                                                        "information that is neccessary to know when "
                                                                        "following a vegan diet.", order=1,
                    imageUrl="https://images.immediate.co.uk/production/volatile/sites/30/2013/07/tofu-6a6a4ef.jpg"
                             "?quality=90&resize=556,505")

    db.session.add(easyQuiz)
    db.session.commit()

    question1 = Question(
        quizID=easyQuiz.quizID,
        questionText="What is tofu made from?",
        correctAnswer="Soybeans",
        otherOptions=["Wheat", "Rice", "Almonds"]
    )

    question2 = Question(
        quizID=easyQuiz.quizID,
        questionText="Which of the following is not a common vegan substitute for milk?",
        correctAnswer="Cows Milk",
        otherOptions=["Oat Milk", "Coconut Milk", "Almond Milk"]
    )

    question3 = Question(
        quizID=easyQuiz.quizID,
        questionText="Which nutrient is most vegans concerned about getting enough of?",
        correctAnswer="Vitamin B12",
        otherOptions=["Protein", "Iron", "Vitamin C"]
    )

    question4 = Question(
        quizID=easyQuiz.quizID,
        questionText="What can be used as a binding agent in vegan baking instead of eggs?",
        correctAnswer="Flax seeds",
        otherOptions=["Water", "Flour", "Sugar"]
    )

    question5 = Question(
        quizID=easyQuiz.quizID,
        questionText="Which of these ingredients is not vegan?",
        correctAnswer="Honey",
        otherOptions=["Cane sugar", "Maple syrup", "Agave syrup"]
    )

    db.session.add(question1)
    db.session.add(question2)
    db.session.add(question3)
    db.session.add(question4)
    db.session.add(question5)


def intermediate_quiz():
    intermediateQuiz = Quiz(quizName="Intermediate Quiz: Cooking Techniques & Ingredients",
                            quizDescription="A quiz designed to test knowledge on vegan cooking techniques and the "
                                            "use of specific ingredients in vegan cuisine.",
                            order=2, imageUrl="https://www.veganfoodandliving.com/wp-content/uploads/2020/03"
                                              "/vegancooking-tips-2.jpg")

    db.session.add(intermediateQuiz)
    db.session.commit()

    question1 = Question(
        quizID=intermediateQuiz.quizID,
        questionText="What is tempeh made from?",
        correctAnswer="Fermented soybeans",
        otherOptions=["Mashed chickpeas", "Compressed vegetable protein", "Ground almonds"]
    )

    question2 = Question(
        quizID=intermediateQuiz.quizID,
        questionText="Which vitamin is often added to plant milks to enhance their nutritional value?",
        correctAnswer="Vitamin D",
        otherOptions=["Vitamin A", "Vitamin C", "Vitamin E"]
    )

    question3 = Question(
        quizID=intermediateQuiz.quizID,
        questionText="What is aquafaba?",
        correctAnswer="The liquid in canned chickpeas",
        otherOptions=["A type of sea vegetable", "A vegan gelatin substitute", "A brand of vegan cheese"]
    )

    question4 = Question(
        quizID=intermediateQuiz.quizID,
        questionText="Which cooking technique can intensify the flavor of vegetables?",
        correctAnswer="Roasting",
        otherOptions=["Boiling", "Steaming", "Freezing"]
    )

    question5 = Question(
        quizID=intermediateQuiz.quizID,
        questionText="Seitan is a popular meat substitute made from what primary ingredient?",
        correctAnswer="Vital wheat gluten",
        otherOptions=["Soy protein isolate", "Textured vegetable protein", "Pea protein"]
    )

    db.session.add(question1)
    db.session.add(question2)
    db.session.add(question3)
    db.session.add(question4)
    db.session.add(question5)
    db.session.commit()


def advanced_quiz():
    advancedQuiz = Quiz(quizName="Advanced Quiz: Specialized Knowledge",
                        quizDescription="An advanced quiz to test detailed knowledge about nutrition and specialized "
                                        "cooking methods in vegan cuisine.",
                        order=3,
                        imageUrl="https://i.pinimg.com/originals/8b/ec/bf/8becbf01d0a258a38ea2f042b9127c52.jpg")

    db.session.add(advancedQuiz)
    db.session.commit()

    question1 = Question(
        quizID=advancedQuiz.quizID,
        questionText="What amino acid is primarily missing in many plant-based proteins and needs to be supplemented?",
        correctAnswer="Methionine",
        otherOptions=["Lysine", "Tryptophan", "Leucine"]
    )

    question2 = Question(
        quizID=advancedQuiz.quizID,
        questionText="Which cooking method best retains the nutrients in vegetables?",
        correctAnswer="Steaming",
        otherOptions=["Frying", "Grilling", "Baking"]
    )

    question3 = Question(
        quizID=advancedQuiz.quizID,
        questionText="Which traditional Japanese ingredient is vegan and used as a flavor enhancer?",
        correctAnswer="Miso",
        otherOptions=["Fish sauce", "Oyster sauce", "Prawn paste"]
    )

    question4 = Question(
        quizID=advancedQuiz.quizID,
        questionText="What is the nutritional benefit of sprouting legumes before eating them?",
        correctAnswer="Enhances protein quality",
        otherOptions=["Increases caloric content", "Reduces vitamin levels", "Increases fat content"]
    )

    question5 = Question(
        quizID=advancedQuiz.quizID,
        questionText="How does fermenting vegetables impact their nutritional value?",
        correctAnswer="Increases B vitamins",
        otherOptions=["Decreases mineral content", "Reduces fiber", "Lowers antioxidant levels"]
    )

    db.session.add(question1)
    db.session.add(question2)
    db.session.add(question3)
    db.session.add(question4)
    db.session.add(question5)
    db.session.commit()
