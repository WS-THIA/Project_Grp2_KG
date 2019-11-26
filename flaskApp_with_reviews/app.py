from flask import Flask, render_template, redirect
from forms import textInterface, radioInterface, recommendationInterface
from py2neo import Graph

burpple = Graph(host="localhost://7474", auth=("neo4j", "123456"))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'myKey123'


def r_recommender(graph, cid, num_nearest_neighbors, num_recommendations):
    query = """
           MATCH (p1:Reviewer)-[:Wrote]->(r1:Review)-[:About]->(re:Restaurant)<-[:About]-(r2:Review)<-[:Wrote]-(p2:Reviewer)
           WHERE p1 <> p2 AND p1.name = {p_name}
           WITH p1, p2, COUNT(DISTINCT re) as intersection

           MATCH (p:Reviewer)-[:Wrote]->(r:Review)-[:About]->(re:Restaurant)
           WHERE p in [p1, p2]
           WITH p1, p2, intersection, COUNT(DISTINCT re) as union

           WITH p1, p2, intersection, union, 
              (intersection * 1.0 / union) as jaccard_index

           ORDER BY jaccard_index DESC, p2.name
           WITH p1, COLLECT(p2)[0..{k}] as neighbors
           WHERE SIZE(neighbors) = {k}                                              
           UNWIND neighbors as neighbor
           WITH p1, neighbor

           MATCH (neighbor)-[:Wrote]->(r:Review)-[:About]->(re:Restaurant)         
           WHERE not (p1)-[:Wrote]->(r:Review)-[:About]->(re:Restaurant)                        
           WITH p1, re, COUNT(DISTINCT neighbor) as countnns
           ORDER BY p1.name, countnns DESC                            
           RETURN p1.name as user, 
              COLLECT(re.name)[0..{n}] as recommendations  
           """

    recommendations = {}

    for i in graph.run(query, p_name=cid, k=num_nearest_neighbors, n=num_recommendations):
        recommendations[i[0]] = i[1]

    return recommendations


def search_restaurant_by_cusine(graph, text, sort):
    result = []
    result_review = {}

    query_rating = """
        MATCH (r:Review)-[a:About]->(re:Restaurant)
        WHERE re.cuisine = {term}
        WITH re,COUNT(r) AS number,SUM(a.restaurant_sentiment) AS senti      

        RETURN re.name, senti/number AS average_senti
        ORDER BY average_senti DESC

    """

    query_popularity = """
        MATCH (r:Review)-[a:About]->(re:Restaurant)
        WHERE re.cuisine = {term}
        WITH re,COUNT(r) AS number        
        RETURN re.name,number
        ORDER BY number DESC

    """

    query_top = """
            MATCH (r:Review)-[a:About]->(re:Restaurant)
            WHERE re.name ={term}
            WITH re, a, r
            ORDER BY a.restaurant_sentiment DESC
            WITH re, COLLECT(r)[0..3] AS top3
            UNWIND top3 AS top
            RETURN re.name, top.review
            """

    query_bottom = """
            MATCH (r:Review)-[a:About]->(re:Restaurant)
            WHERE re.name = {term}
            WITH re, a, r
            ORDER BY a.restaurant_sentiment DESC
            WITH re, COLLECT(r)[-4..-1] AS bottom3
            UNWIND bottom3 AS bottom
            RETURN re.name, bottom.review
            """
    if sort == 'number_of_reviews':
        query = query_popularity

    if sort == 'rating':
        query = query_rating

    ans = graph.run(query, term=text).data()
    if not ans:
        return ['No records found']
    else:
        for item in ans:
            result.append(item['re.name'])
            result_review[item['re.name']] = []

        for res in result:
            t = []
            b = []

            temp_t = graph.run(query_top, term=res).data()
            for element in temp_t:
                result_review[element['re.name']].append(element['top.review'])

            temp_b = graph.run(query_bottom, term=res).data()
            for element in temp_b:
                result_review[element['re.name']].append(element['bottom.review'])

        return result_review


def search_restaurant_by_food(graph, text, sort):
    result = []
    key_words = text
    result_review = {}

    query_rating = """
        MATCH (r:Review)-[c:Contains]->(f:Food)
        WHERE f.name = {term}
        WITH DISTINCT r, c
        MATCH (r)-[a:About]->(re:Restaurant)
        RETURN re.name, sum(c.food_sentiment)/count(r) AS average_senti, count(r) AS number
        ORDER BY average_senti DESC
        """
    query_popularity = """
        MATCH (r:Review)-[c:Contains]->(f:Food)
        WHERE f.name = {term}
        WITH DISTINCT r, c
        MATCH (r)-[a:About]->(re:Restaurant)
        RETURN re.name, sum(c.food_sentiment)/count(r) AS average_senti, count(r) AS number
        ORDER BY number DESC
        """

    query_top = """
            MATCH (r:Review)-[a:About]->(re:Restaurant)
            WHERE re.name = {restaurant}
            WITH re, a, r
            MATCH (r:Review)-[c:Contains]->(f:Food)
            WHERE f.name = {food}
            WITH re, r, c
            ORDER BY c.food_sentiment DESC
            WITH re, COLLECT(r)[0..3] AS top3
            UNWIND top3 AS top
            RETURN re.name, top.review
            """

    query_bottom = """
                MATCH (r:Review)-[a:About]->(re:Restaurant)
                WHERE re.name = {restaurant}
                WITH re, a, r
                MATCH (r:Review)-[c:Contains]->(f:Food)
                WHERE f.name = {food}
                WITH re, r, c
                ORDER BY c.food_sentiment DESC
                WITH re, COLLECT(r)[-4..-1] AS bottom3
                UNWIND bottom3 AS bottom
                RETURN re.name, bottom.review
                """

    if sort == 'number_of_reviews':
        query = query_popularity

    if sort == 'rating':
        query = query_rating

    ans = graph.run(query, term=text).data()

    if ans:
        for item in ans:
            result.append(item['re.name'])
            result_review[item['re.name']] = []

        for res in result:
            t = []
            b = []

            temp_t = graph.run(query_top, restaurant=res, food=key_words).data()
            for element in temp_t:
                result_review[element['re.name']].append(element['top.review'])

            temp_b = graph.run(query_bottom, restaurant=res, food=key_words).data()
            for element in temp_b:
                result_review[element['re.name']].append(element['bottom.review'])

        return result_review

    if not ans:
        key_words = key_words.split()
        result = {}

        for i in range(len(key_words)):
            temp = graph.run(query, term=key_words[i]).data()
            result[key_words[i]] = []
            for item in temp:
                result[key_words[i]].append(item['re.name'])

        if not result:
            return ['No records found']
        else:
            for res in result:
                t = []
                b = []

                temp_t = graph.run(query_top, restaurant=res, food=key_words).data()
                for element in temp_t:
                    result_review[element['re.name']].append(element['top.review'])

                temp_b = graph.run(query_bottom, restaurant=res, food=key_words).data()
                for element in temp_b:
                    result_review[element['re.name']].append(element['bottom.review'])

            return result_review


###### Function here ######
def QueryFunction(food_text, sortBy):
    food_text = food_text.lower()
    res = search_restaurant_by_food(burpple, food_text, sortBy)

    return res


def Cuisine_query(cuisine_txt, sortBy):
    print(cuisine_txt)
    cuisine_txt = cuisine_txt.lower()
    res = search_restaurant_by_cusine(burpple, cuisine_txt,sortBy)

    return res


def makeRecommendation(userID):
    print(userID)
    res = r_recommender(burpple, userID, 10, 5)

    return res


###### End Function ######

@app.route('/', methods=['GET','POST'])
def main():

    form1 = textInterface()

    form2 = radioInterface()

    form3 = recommendationInterface()

    if form1.validate_on_submit():

        food = form1.textInput.data
        sortBy = form1.sortBy.data
        data = QueryFunction(food, sortBy)
        return render_template('reviews.html', data=data)

    if form2.validate_on_submit():

        cuisine = form2.cuisine.data
        sortBy = form1.sortBy.data
        data = Cuisine_query(cuisine, sortBy)

        return render_template('reviews.html', data=data)

    if form3.validate_on_submit():

        userID = form3.userID.data

        userID = 'U' + userID

        data = makeRecommendation(userID)

        return render_template('reviews.html', data=data)

    return render_template('index.html', form1=form1, form2=form2, form3=form3)


if __name__ == '__main__':
    app.run(debug=True)