from flask import Flask, render_template, request, redirect
from .Queries import *
app = Flask(__name__)
#Calls function that connects to the database and loads all data onto the database
#At initialization of the app the user is first directed to the home page
################## Main Page ####################
@app.route('/')
def Home():
    return render_template('Home.html')
################## Home Pages ###################
@app.route('/Home/Common')
def Home_Common():
    return render_template('Search/Home-Common.html')

@app.route('/Home/Virus')
def Home_Virus():
    return render_template('Search/Home-Virus.html')

@app.route('/Home/Motif')
def Home_Motif():
    return render_template('Search/Home-Motif.html')
################ Search Results #################
@app.route('/Scientific Name/Result/', methods=['GET'])
def search_results_Scientific():
    searchs = request.args.get('search')
    Results = search_scientific(searchs)
    return render_template("Result/Scientific-Result.html",Results = Results)
    
@app.route('/Common Name/Result/', methods=['GET'])
def search_results_Common():
    searchs = request.args.get('search')
    Results = search_full(searchs)
    return render_template("Result/Common-Result.html",Results = Results)

@app.route('/Virus/Result/', methods=['GET'])
def search_results_Virus():
    searchs = request.args.get('search')
    Results = search_virus(searchs)
    return render_template("Result/Virus-Result.html",Results = Results)

@app.route('/Motif/Result/', methods=['GET'])
def search_results_Motif():
    searchs = request.args.get('search')
    Results = search_motif(searchs)
    return render_template("Result/Motif-Result.html",Results = Results)
################ About Page #####################
@app.route('/About/')
def About():
    return render_template('About/About.html')
################## View Plants ##################
@app.route('/Plants/')
def Plants():
    Plants = get_plants()
    return render_template('Browse/Plants/Plants.html', Plants = Plants)
################## View Viruses #################
@app.route('/Viruses/')
def Viruses():
    Viruses = get_viruses()
    return render_template('Browse/Viruses/Viruses.html', Viruses = Viruses)
################ View Infects ###################
@app.route('/Infects/')
def Infects():
    Infects = get_infects()
    return render_template('Browse/Infects/Infects.html', Infects = Infects)
################## View CDS #####################
@app.route('/CDS/')
def CDS():
    CDS = get_CDS()
    return render_template('Browse/CDS/CDS.html', CDS = CDS)
############### View motifs-domain ##############
@app.route('/motifs_domain/')
def motifs_domain():
    CDSresult = get_motifs_domain()
    return render_template('Browse/motifs_domain/motifs_domain.html', CDSresult = CDSresult)
#################################################
if __name__ == '__main__':
    app.run(debug=True)

