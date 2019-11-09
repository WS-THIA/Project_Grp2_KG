from flask import Flask, render_template, redirect
from forms import textInterface, radioInterface

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myKey123'

###### Function here ######
def QueryFunction(food_text):

    # query here

    # convert to data frame

    #return the dataframe
    return food_text + ' testing'

###### End Function ######

@app.route('/', methods=['GET','POST'])
def main():

    form1 = textInterface()

    form2 = radioInterface()

    if form1.validate_on_submit():
        food = form1.textInput.data

        # Call function here
        data = QueryFunction(food)

        return render_template('reviews.html', data = data)

    return render_template('index.html', form1=form1, form2=form2)

@app.route('/reviews')
def reviews():

    return render_template('reviews.html')

if __name__ == '__main__':
    app.run(debug=True)