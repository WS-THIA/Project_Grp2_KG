from flask import Flask, render_template, redirect
from forms import textInterface, radioInterface, recommendationInterface

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myKey123'

###### Function here ######
def QueryFunction(food_text):


    #return the dataframe
    return food_text + ' testing'

def Cuisine_query(cuisine_txt):


    return cuisine_txt + str(12345)

def makeRecommendation(userID):

    return userID + str(123)

###### End Function ######

@app.route('/', methods=['GET','POST'])
def main():

    form1 = textInterface()

    form2 = radioInterface()

    form3 = recommendationInterface()

    if form1.validate_on_submit():

        food = form1.textInput.data

        # Call function here
        data = QueryFunction(food)
        return render_template('reviews.html', data=data)

    if form2.validate_on_submit():

        cuisine = form2.cuisine.data

        data = Cuisine_query(cuisine)

        return render_template('reviews.html', data=data)

    if form3.validate_on_submit():

        userID = form3.userID.data

        userID = 'U' + userID

        data = makeRecommendation(userID)

        return render_template('reviews.html', data=data)

    return render_template('index.html', form1=form1, form2=form2, form3=form3)


if __name__ == '__main__':
    app.run(debug=True)