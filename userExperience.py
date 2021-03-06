# Web scraper in Python
# Tutorial from - https://www.topcoder.com/thrive/articles/web-crawler-in-python

# USER EXPERIENCE SEQUENCE USE FILE - Read the README.md file for explanations on how to use

################################################### IMPORTS ################################################

from PIL import ImageTk, Image as im, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from utils import *
from tkinter import *
from os import listdir
from os.path import isfile, join

##################################################### UEM FUNCTIONS ###########################################

# Function returning the list of existing user experience models
def getUEMList() :
    # We get all the files in the userExperiencesModels folder
    path = "UEM/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    # We now strip the .csv part from the file names to make them more presentable
    for i in range(len(onlyfiles)) :
        onlyfiles[i] = onlyfiles[i].split('.')[0].split('_')[1]

    # We return the files names
    return onlyfiles

# Function returning the list of existing user experience models
def getUEMIngsList() :
    # We get all the files in the userExperiencesModels folder
    path = "UEMIngs/"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    # We now strip the .csv part from the file names to make them more presentable
    for i in range(len(onlyfiles)) :
        onlyfiles[i] = onlyfiles[i].split('.')[0].split('_')[1]

    # We return the files names
    return onlyfiles

#################################################### MAIN FUNCTION ###########################################

# Main function
def main() :
    # Welcome message
    print("Welcome to the User Experience Sequence interface.\n")

    # We ask the user to choose a name for data collection purpose
    username = "Anonymous"

    # Correct input variable
    redoInput = True

    # Selection loop
    while (redoInput) :
        # We ask the user to choose a model
        print("Please select a username :\n(You may press Enter without giving a name in case you prefer to remain anonymous)")
        sel = input()

        # We check if the chosen ID is valid
        if (sel == "") :
            redoInput = False
            username = sel
        
        # In case the name is too long, we ask the user to select a different name
        elif (len(sel) > 16) :
            print("\nPlease select a shorter username.")

        else :
            redoInput = False
            username = sel


    # We ask the user to if he wants to add the ingredients to the UE
    withIngredients = False

    # Correct input variable
    redoInput = True

    # Selection loop
    while (redoInput) :
        # We ask the user to choose a model
        print("\nWould you like to have the recipes' ingredient lists shown ?\n(0 - No, 1 - Yes)")
        sel = input()

        # We use the ingredients
        if (sel == "1") :
            redoInput = False
            withIngredients = True

        # We don't use the ingredients
        elif (sel == "0") :
            redoInput = False
            withIngredients = False

        # We make the user choose again
        else :
            print("\nPlease answer with either 0 (No) or 1 (Yes).")


    # We collect all the models IDs
    if (withIngredients) :
        models = getUEMIngsList()
    else :
        models = getUEMList()

    # We verify that at least one model exists
    if (len(models) == 0) :
        print("\nWe couldn't find any models in the corresponding folder ('userExperiencesModels').\nPlease check your files.\n")
        print("Exiting the interface ...")
        return

    # We ask the user to select a model
    print("\nPlease select a model from the existing ones :")
    for i in models :
        print("\t> " + i)

    # Correct input variable
    redoInput = True
    selectedModel = 0

    # Selection loop
    while (redoInput) :
        # We ask the user to choose a model
        print("\nPlease enter a model ID :")
        sel = input()

        # We check if the chosen ID is valid
        if (sel in models) :
            redoInput = False
            selectedModel = sel
            print("\nThe user experience will soon begin. A window should appear on your screen.")
        
        # In case the selected ID is wrong, we ask the user to try again
        else :
            print("\nThe selected ID does not exist.\nPlease select a model from the existing ones :")
            for i in models :
                print("\t> " + i)

##################################################### WINDOW CREATION ########################################

    # declare the window
    window = Tk()

    # set window title
    window.title("User Experience")
    window.configure(bg='#7C7A7A')
    window.geometry("300x200")
    window.resizable(False, False)

################################################### GLOBAL PARAMETERS ########################################

    # Questionnary values
    answerList = list()

    # We extract all the data from the user experience data file
    # We also extract all the data from the recipes
    uemdata = None
    if (withIngredients) :
        uemdata = pd.read_csv("UEMIngs/model_" + selectedModel + "_ingredients.csv")
    else :
        uemdata = pd.read_csv("UEM/model_" + selectedModel + ".csv")

    # List of recipe ids
    recipeA_ids = uemdata["recipe_A_id"].tolist()
    recipeB_ids = uemdata["recipe_B_id"].tolist()

    # List of recipe names
    recipeA_names = uemdata["recipe_A_name"].tolist()
    recipeB_names = uemdata["recipe_B_name"].tolist()

    # List of recipe pictures
    recipeA_picture_list = uemdata["recipe_A_picture"].tolist()
    recipeB_picture_list = uemdata["recipe_B_picture"].tolist()

    # We generate all the pictures
    for i in range(len(recipeA_picture_list)) :
        recipeA_picture_list[i] = ImageTk.PhotoImage(im.open(recipeA_picture_list[i]))
    for i in range(len(recipeB_picture_list)) :
        recipeB_picture_list[i] = ImageTk.PhotoImage(im.open(recipeB_picture_list[i]))

    # We also extract the ingredients if needed
    recipeA_ings = []
    recipeB_ings = []
    if (withIngredients) :
        recipeA_ings = uemdata["recipe_A_ingredients"].tolist()
        recipeB_ings = uemdata["recipe_B_ingredients"].tolist()

        for i in range(len(recipeA_ings)) :
            recipeA_ings[i] = recipeA_ings[i].replace('\u2009', ' and ').split('#')
            recipeB_ings[i] = recipeB_ings[i].replace('\u2009', ' and ').split('#')

    # We extract all the correct answers
    expAnswers = uemdata["correct_answer"].tolist()

##################################################### UTILS FUNCTIONS ########################################

    # Function - Close window
    def closeWindow() :
        window.quit()

    # Function - Clear window
    def clearWindow() :
        for i in window.winfo_children() :
            i.destroy()

##################################################### INIT SEQUENCE ##########################################

    # Functions
    # First window setup
    def initWindow() :
        Label(window, text="User Experience - Food Questions", justify=CENTER).place(relx=0.5, rely=0.1, anchor=CENTER)
        start_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # Start questionnary
    def startQuestionnary() :
        # We clear the window
        clearWindow()

        # We prepare the first question
        if withIngredients :
            window.geometry("1000x1000")
        else :
            window.geometry("1000x800")
        questionSequence(0)

    # Entries and buttons
    start_button = Button(window, text="Start", command=startQuestionnary)

################################################## QUESTION SEQUENCE ###########################################

    # Functions
    # Show the choice situation number questionID
    def questionSequence(questionID) :
        # We clear the window
        clearWindow()

        # We create the checkboxes and the IntVar variables
        choiceA = IntVar() # Represents the value 1
        choiceABox = Checkbutton(window, text=recipeA_names[questionID], variable=choiceA)

        choiceB = IntVar() # Represents the value 2
        choiceBBox = Checkbutton(window, text=recipeB_names[questionID], variable=choiceB)

        pictureChoice = IntVar() # Represents the value 1
        pictureChoiceBox = Checkbutton(window, text="The pictures", variable=pictureChoice)

        nameChoice = IntVar() # Represents the value 2
        nameChoiceBox = Checkbutton(window, text="The names", variable=nameChoice)

        ingredientsChoice = IntVar()
        ingredientsChoiceBox = Checkbutton(window, text="The ingredients", variable=ingredientsChoice)

        # Function to check if the necessary boxes have been checked
        def validSelection() :
            return (choiceA.get() + choiceB.get() == 1) and (pictureChoice.get() + nameChoice.get() + ingredientsChoice.get() == 1)

        # Function returning a tuple containing the choices the user made
        def saveChoices() :
            # Creating the variables
            rC = 0
            rI = 0

            # Saving the recipe choice
            if (choiceA.get() == 1) :
                rC = 1
            else :
                rC = 2

            # Saving the info choice
            if (pictureChoice.get() == 1) :
                rI = 1
            elif (nameChoice.get() == 1) :
                rI = 2
            else :
                rI = 3

            # Return the choice tuple
            return rC, rI

        # Function to go to the next
        def goToNextQuestion() :
            if (validSelection()) :
                # Saving the selection*
                tmpC, tmpI = saveChoices()
                answerList.append([questionID, recipeA_ids[questionID], recipeB_ids[questionID], tmpC, tmpI, expAnswers[questionID]])

                # Ending the questionnary
                if (questionID + 1 >= len(recipeA_names)) :
                    endWindow()

                # Moving to the next question
                else :
                    questionSequence(questionID + 1)

        # Question title
        Label(window, text="Choice " + str(questionID + 1), justify=CENTER).pack(side=TOP)
        Label(window, text="In your opinion, which recipe contains the most fat per serving?", justify=CENTER).pack(side=TOP)

        # We show the recipes' pictures
        Label(window, image=recipeA_picture_list[questionID]).place(x=100, y=200)
        Label(window, image=recipeB_picture_list[questionID]).place(x=600, y=200)

        # We show the recipes' names
        choiceABox.place(x=100, y=510)
        choiceBBox.place(x=600, y=510)

        # We show the recipe ingredients
        ListIngsA = Listbox(window, width=50)
        ListIngsB = Listbox(window, width=50)
        if (withIngredients) :
            # We update the recipe A list
            for e in recipeA_ings[questionID] :
                ListIngsA.insert(END, e)
            ListIngsA.place(x=100, y=550)

            # We update the recipe A list
            for e in recipeB_ings[questionID] :
                ListIngsB.insert(END, e)
            ListIngsB.place(x=600, y=550)
            

        # We ask about what helped the user decide and add the next button
        Button(window, text="Next", command=goToNextQuestion).pack(side=BOTTOM)
        nameChoiceBox.pack(side=BOTTOM)
        pictureChoiceBox.pack(side=BOTTOM)
        if (withIngredients) :
            ingredientsChoiceBox.pack(side=BOTTOM)
        Label(window, text="Which information helped you choose ?").pack(side=BOTTOM)
    

################################################# QUESTIONNARY END #############################################

    # Final window
    def endWindow() :
        # We clear the window
        clearWindow()

        # Saving the results in the results file
        if (withIngredients) :
            resultsfn = "results_" + username + "_" + str(np.random.randint(0, 1000)) + "_ingredients.csv"
        else :
            resultsfn = "results_" + username + "_" + str(np.random.randint(0, 1000)) + ".csv"

        # We open the .csv file
        with open(resultsfn, 'w', encoding='utf8') as f :
            # We create a writer
            writer = csv.writer(f)

            # We write the header
            writer.writerow(["question_id", "recipe_A_id", "recipe_B_id", "recipe_choice", "information_choice", "expected_answer"])

            # We write the result of the experience
            writer.writerows(answerList)

        # We resize the window
        window.geometry("300x200")

        # Thanks for participating
        Label(window, text="Thanks for participating !\nYou can find the results of the questionnary\nin the " + resultsfn + " file.", justify=CENTER).place(relx=0.5, rely=0.3, anchor=CENTER)
        Button(window, text="Exit", command=closeWindow).place(relx=0.5, rely=0.8, anchor=CENTER)

################################################## INIT PART ###############################################

    # Showing the window
    initWindow()
    window.mainloop()

    # END OF MAIN FUNCTION

################################################## MAIN PART ###################################################

if __name__ == "__main__" :
    main()
