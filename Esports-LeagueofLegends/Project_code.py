"""
Code for the Project: E-Sport Analytics and Predictions
for League of Legends
by Ritwik Katiyar
"""
# Imports
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn import metrics
import plotly.express as px
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
# Initializing seaborn
sns.set()


def plot_world_tiers():
    """
    Generates a plot for regions at worlds based on the region's tier
    """
    # Create a list that repeats Tier 2, 39 times. For all European counties
    col = ['Tier 2'] * 39
    # Add Tier 1 to the front of the list
    col[0:1] = ['Tier 1', 'Tier 1']
    # Add tier 3, tier 4, and tier 5 to the end of the list
    col = col + ['Tier 3', 'Tier 3']+['Tier 4', 'Tier 4', 'Tier 4'] + \
        ['Tier 5', 'Tier 5', 'Tier 5', 'Tier 5', 'Tier 5', 'Tier 5', 'Tier 5']
    # Create a list of county names that take part at the world championships
    loc = ['China', 'South Korea', 'UK', 'France', 'Spain', 'Portugal',
           'Belgium', 'Ierland', 'Luxembourg', 'Netherlands', 'Germany',
           'Switzerland', 'Austria', 'Italy', 'Iceland', 'Norway',
           'Sweden', 'Denmark', 'Finland', 'Estonia', 'Latvia', 'Lithuania',
           'Belarus', 'Poland', 'Czech Republic', 'Slovakia', 'Hungary',
           'Ukraine', 'Moldova', 'Slovenia', 'Croatia', 'Bosnia', 'Romania',
           'Serbia', 'Montenegro', 'Kosovo', 'Macedonia', 'Bulgaria',
           'Albania', 'Greece', 'USA', 'Canada', 'Vietnam', 'Taiwan',
           'Philippines', 'Japan', 'Brazil', 'Australia',
           'Latin America', 'Turkey', 'Russia', 'Mexico']
    # Use plotly in order to generate a plot
    fig = px.choropleth(locations=loc, locationmode="country names", color=col,
                        color_discrete_sequence=["#7E2F8E", "#0072BD",
                                                 "#A2142F", "#D95319",
                                                 "#EDB120"])
    # Edit the plotly plot and make minor changes
    fig.update_layout(
        geo=dict(
            # removes the frame
            showframe=False,
            # removes cost lines
            showcoastlines=False,
            # sets a type of world map
            projection_type='equirectangular'
        ),)
    # fig.show()


def total_games(game_end_stats):
    """
    Returns the total length of the game by dividing the length of
    cumulative team match data by 2
    """
    return len(game_end_stats)/2


def pick_rate_func(individual_stats, total_games):
    """
    Returns the pick rate for all the champions at worlds that
    were played at least 5 times or more.
    """
    # Get the amount of times a champion was picked
    pick_rate = individual_stats['champion'].value_counts()
    # Remove champions that were picked less than 5 times
    pick_rate = pick_rate.loc[lambda x: (x >= 5)]
    # Get the total number of games at worlds
    """
    Pick rate of a champion is the number of games the champion was picked
    over the total number of games at worlds
    """
    return pick_rate/total_games


def ban_rate_func(game_end_stats, total_games):
    """
    Returns the ban rate for all the champions at worlds that
    were banned at least 5 times or more.
    """
    # Get the ban rate for the ban1 column for every champion
    ban_rate_1 = game_end_stats['ban1'].value_counts()
    # Get the ban rate for the ban2 column for every champion
    ban_rate_2 = game_end_stats['ban2'].value_counts()
    # Get the ban rate for the ban3 column for every champion
    ban_rate_3 = game_end_stats['ban3'].value_counts()
    # Get the ban rate for the ban4 column for every champion
    ban_rate_4 = game_end_stats['ban4'].value_counts()
    # Get the ban rate for the ban5 column for every champion
    ban_rate_5 = game_end_stats['ban5'].value_counts()
    # combine all the ban rates 1-5 together into a data frame
    ban_rate = pd.concat([ban_rate_1, ban_rate_2, ban_rate_3,
                          ban_rate_4, ban_rate_5], axis=1)
    # For any champion that wasn't banned in ban1-5 replace N/A into 0
    ban_rate = ban_rate.fillna(0)
    # Sum up the values for every champion for each ban
    ban_rate = ban_rate.loc[:, 'ban1'] + ban_rate.loc[:, 'ban2'] + \
        ban_rate.loc[:, 'ban3'] + ban_rate.loc[:, 'ban4'] + \
        ban_rate.loc[:, 'ban5']
    # Remove any champion that were banned less than 5 times
    ban_rate = ban_rate.loc[lambda x: (x >= 5)]
    # Calculate the ban rate by dividing from the total games
    return ban_rate/total_games


def win_rate_func(individual_stats):
    """
    Returns the win rate for all the champions at worlds that
    were won at least 5 games.
    """
    """
    Filter the data where the result column is 1.
     i.e the result of the game was a win
     """
    individual_stats_win = individual_stats[(individual_stats['result'] == 1)]
    # count the amount of times a champion appears
    win_rate = individual_stats_win['champion'].value_counts()
    # Remove champions that had less than 5 games won
    win_rate = win_rate.loc[lambda x: (x >= 5)]
    # Get the amount of times the champion was picked at worlds
    new_pr = individual_stats['champion'].value_counts()
    # combine the two columns together
    win_rate = pd.concat([win_rate, new_pr], axis=1)
    # drop any values that appear as N/A
    win_rate = win_rate.dropna()
    """
    Divide column 0 (number of wins) by column 1
    (Number of times a champion was picked)
    """
    return win_rate.iloc[:, 0] / win_rate.iloc[:, 1]


def pick_ban_win_rates_func(pick_rate, ban_rate, win_rate):
    """
    Combines the restuls from pick rate, win rate and ban rate functions above
    """
    # Convert the pick_rate from a series to a data frame
    picks = pick_rate.to_frame()
    # Convert the index into a column
    picks['Champions'] = picks.index
    # drop the old index
    picks.reset_index(drop=True, inplace=True)
    # rename the pick rate column
    picks.rename(columns={picks.columns[0]: 'pick_rate'}, inplace=True)
    # convert the ban_rate from a series to a data frame
    bans = ban_rate.to_frame()
    # convert the index into a column
    bans['Champions'] = bans.index
    # drop the old index
    bans.reset_index(drop=True, inplace=True)
    # rename the ban rate column
    bans.rename(columns={bans.columns[0]: 'ban_rate'}, inplace=True)
    # Convert win rate series into a data frame
    wins = win_rate.to_frame()
    # convert the index into a column
    wins['Champions'] = wins.index
    # drop the old index
    wins.reset_index(drop=True, inplace=True)
    # Rename the win rates column as win_rate
    wins.rename(columns={wins.columns[0]: 'win_rate'}, inplace=True)
    """
    Make a new merged data frame that joins the picks and
    bans data frames together. Perform a left join in order
    to keep all the champions
    """
    pick_bans = pd.merge(picks, bans, on='Champions', how='left')
    # Re-order the columns
    pick_bans = pick_bans[['Champions', 'pick_rate', 'ban_rate']]
    """
    Perform another merge and add wins data frame to the data frame.
    Perform a left join in order to keep all the champions
    """
    pick_ban_win = pd.merge(pick_bans, wins, on='Champions', how='left')
    # Replace any na values within win_rate column with 0.0 floating point type
    pick_ban_win['win_rate'] = pick_ban_win['win_rate'].fillna(0.0)
    # Replace any na values within win_rate column with 0.0 floating point type
    pick_ban_win['ban_rate'] = pick_ban_win['ban_rate'].fillna(0.0)
    #  convert the index into a column
    pick_ban_win.index = pick_ban_win['Champions']
    """
    sort by descending order for pick rate and win rate;
    Also, sort in ascending order for ban rate
    """
    pick_ban_win = pick_ban_win.sort_values(by=['pick_rate', 'ban_rate',
                                                'win_rate'],
                                            ascending=[False, True, False])
    # take only the top 30 champions out of all the champions in the data frame
    return pick_ban_win.iloc[:30, 1:]


def plot_pick_ban_wins(pick_ban_win):
    """
    Generates the heat map for the top 30 champions with highest
    pick rate, lowest ban rate and highest win rate.
    """
    # Declare a set figure size for the plot
    f, ax = plt.subplots(1, 1, figsize=(8, 6.5))
    # Create a list of x- axis labes for the plot
    x_labs = ['Pick Rate', 'Ban Rate', 'Win Rate']
    # initialize the heat map plot with the figure size
    sns.heatmap(pick_ban_win, linewidths=0.5, annot=True, cbar=False,
                cmap="flare", xticklabels=x_labs, fmt="1.0%", ax=ax)
    # Provide a title for the plot
    plt.title('Top 30 Champions With Highest Pick,Ban and Win Rate at Worlds')
    plt.savefig('pick_ban_wins.png', bbox_inches='tight')


def plot_champs_at_worlds(player_name, individual_stats):
    """
    Plots the number of times each champion was played by a player at worlds
    """
    # Filter the data set by the player name
    player_at_worlds = individual_stats[
                        (individual_stats['playername'] == player_name)]
    # Just getting the champion column
    player_at_worlds = player_at_worlds.loc[:, ('champion')]
    # Count the times the player played the champions
    player_at_worlds = player_at_worlds.value_counts()
    # set figure size
    f, ax = plt.subplots(1, 1, figsize=(6, 5))
    # Create a bar plot
    sns.barplot(x=player_at_worlds.index,
                y=player_at_worlds.values,
                ax=ax, palette="mako")
    plt.xticks(rotation=-45)
    plt.xlabel("Champions")
    plt.ylabel("Amount of Games Played")
    plt.title('Champions played at Worlds')
    plt.savefig('Champs_at_worlds.png', bbox_inches='tight')


def player_champ_prob_model(player_name, df):
    """
    filter the original data frame by individual
    player data, From the summer split
    Where the regional league is Korea,China,North America and Europe.
    """
    player_champs = df[(df['position'] != "team") &
                       ((df['split'] == "Summer")) &
                       ((df['league'] == 'LCK') | (df['league'] == 'LCS') |
                        (df['league'] == 'LPL') | (df['league'] == 'LEC'))]
    """
    Filter the columns that we need. That being playername,
    champion they played and the result of the game
    """
    player_champs = player_champs.loc[:, ('playername', 'champion', 'result')]
    # Filter by a specific player
    player = player_champs[(player_champs['playername'] == player_name)]
    # Reset the index to start from 0
    player.reset_index(drop=True, inplace=True)
    # get the number of times a champion was played by the player
    unique_champs = player['champion'].nunique()
    # Get the names of all the unique champions the player plays
    player_champs = player['champion'].unique()
    # convert the series into a data frame of champions
    player_champs = pd.DataFrame(player_champs, columns=['Champions'])
    # Sort the champions by alphabetical order
    player_champs = player_champs['Champions'].sort_values(ascending=True)
    # Reset the index
    player_champs.reset_index(drop=True, inplace=True)
    # One hot encode the champions and the result columns
    player = pd.get_dummies(player, columns=['champion', 'result'])
    # Include all the one hot encoded champions as predictors
    X = player.iloc[:, 1:-2]
    # Include all the results where the player won as the target variable
    Y = player.iloc[:, -1]
    # Initialize and name the model
    log_regression = LogisticRegression()
    # fit the data onto the model
    log_regression.fit(X, Y)
    # Prints the intercept for the model
    # print('Intercept :', log_regression.intercept_, "\n")
    # Prints the coefficient for the model
    # print('Coefficient: ', log_regression.coef_, "\n")
    # Use the model to try and predict the results
    pred = log_regression.predict(X)
    """
    Generate the accuracy score of the model by
    constructing a confusion matrix.
    """
    """
    To generate the probabilities for every champion we need a new set of data
    Hence, create a numpy array of the length of champions the player plays
    """
    nparray = np.empty(unique_champs)
    # Fill the array with 1's
    nparray.fill(1)
    # Make sure all the values are of type int and not float
    nparray = nparray.astype(int)
    """
    Convert the 1d array into a matrix with the
    same number of rows and columns as the array
    """
    nparray = np.diag(nparray)
    # convert the matrix into a data frame
    champ = pd.DataFrame(nparray)
    """
    add the column name for the now converted
    matrix by using the player champs data frame
    """
    # that was processed earlier
    champ.columns = X.columns
    # predict the probabilities for every champion
    prob = log_regression.predict_proba(champ)
    # get the win probabilities only
    prob = prob[:, 1]
    # convert the array into a data frame
    prob = pd.DataFrame(prob, columns=['Probability_of_Win'])
    # add champion name for each probability
    prob['Champion'] = player_champs
    # sort the data frame by the least probability of win on top
    prob = prob.sort_values(by='Probability_of_Win', ascending=True)
    # plot the probabilities as a bar plot
    # f, ax = plt.subplots(1, 1, figsize=(5, 3))
    # sns.barplot(data=prob, x="Probability_of_Win",
    #            y="Champion", orient="h", ax=ax,
    #            palette="mako_r")
    # plt.xlabel("Probability of Win")
    # plt.title('Probability of Win Per Champion')
    # plt.savefig('prob_of_win.png', bbox_inches='tight')
    return round(accuracy_score(Y, pred), 2)


def list_of_model_scores(individual_stats, df):
    """
    Returns a list of model scored for every player that attended worlds
    """
    # Filter the data set by the teams from the top four leagues
    regional_players = df[(df['position'] != "team") &
                          ((df['split'] == "Summer")) &
                          ((df['league'] == 'LCK') | (df['league'] == 'LCS') |
                           (df['league'] == 'LPL') | (df['league'] == 'LEC'))]
    # remve any duplicates for players within the filtered data set
    regional_players = regional_players['playername'].drop_duplicates()
    # Get a list of players that played at worlds
    player_names = individual_stats['playername'].unique()
    # transform from a numpy array into a data frame
    player_names = pd.DataFrame(player_names, columns=['playername'])
    # Merge the two data sets, regional players and worlds players.
    # Only get the players that attended worlds
    new_names = pd.merge(regional_players, player_names,
                         on='playername', how='inner')
    # Convert the data frame into a list
    new_names = list(new_names['playername'])
    # initialize a new list
    model_scores = []
    # for every player in the list
    for player in new_names:
        # run a model and get a accuracy score for the player
        model_scores.append(player_champ_prob_model(player, df))
    # return the list of accuracy scores
    return model_scores


def pob_of_win_total_gold(df):
    """
    Makes a model that can predict the probabilty of win based on
    the amount of gold earned.
    """
    # Get the values from the summer and spring splits
    # from the top 4 regions
    gold = df[(df['position'] == "team") &
              ((df['split'] == "Summer") | (df['split'] == "Spring")) &
              ((df['league'] == 'LCK') | (df['league'] == 'LCS') |
              (df['league'] == 'LPL') | (df['league'] == 'LEC'))]
    # remove all other variables
    gold = gold.loc[:, ('totalgold', 'result')]
    # generate the model
    logreg_stats = smf.glm(formula='result ~ totalgold', data=gold,
                           family=sm.families.Binomial()).fit()
    # plot the regression curve for the model
    f, ax = plt.subplots(1, 1, figsize=(4, 4))
    sns.regplot(x=gold['totalgold'], y=gold['result'], logistic=True, ci=None,
                scatter_kws={'color': 'black'}, line_kws={'color': 'red'},
                ax=ax)
    plt.xticks(rotation=45)
    plt.title("Logistic Regression Curve For Gold Earned vs.\
Probability of Winning")
    plt.ylabel('Win (1) vs. Loss (0)')
    plt.xlabel('Total Gold Earned by a Team')
    plt.savefig('reg_curve.png', bbox_inches='tight')

    # Predicts the outcome for the data
    logreg_stats_pred_prob = logreg_stats.predict()
    # if the value is below 0.5 consider that as a loss
    # else consider it as a win
    logreg_stats_pred_class = [('0' if prob < 0.5 else '1')
                               for prob in logreg_stats_pred_prob]
    # Generate a confustion matrix and compare the model predicted values to
    # the actual values
    conf_mat = metrics.confusion_matrix(gold.result.astype(str),
                                        logreg_stats_pred_class)
    # convert the matrix into a data frame
    conf_mat = pd.DataFrame(conf_mat)
    # a list for the matrix
    matrix_index = ['Positive', 'Negative']
    # change the column names to that of the list
    conf_mat.columns = matrix_index
    # change the row names to that of the list
    conf_mat.index = matrix_index
    # print the confusion matrix data frame
    print(conf_mat)
    # print the accuracy score of the model
    print("Accuracy score for the model: ",
          round(accuracy_score(gold.result.astype(str),
                               logreg_stats_pred_class), 2))
    return logreg_stats


def predict_win_teams(df, team1, team2, logreg_stats):
    team_1 = df[(df['position'] == "team") &
                ((df['split'] == "Summer") | (df['split'] == "Spring")) &
                ((df['teamname'] == team1))]
    team_2 = df[(df['position'] == "team") &
                ((df['split'] == "Summer") | (df['split'] == "Spring")) &
                ((df['teamname'] == team2))]
    team_1 = np.array(team_1['totalgold'].mean())
    team_2 = team_2['totalgold'].mean()
    team_1 = logreg_stats.predict(exog=dict(totalgold=team_1))
    team_2 = logreg_stats.predict(exog=dict(totalgold=team_2))
    print("Probabilty of win for", team1, ":", team_1.values,  "\n")
    print("Probabilty of win for", team2, ":", team_2.values, "\n")


def main():
    plot_world_tiers()
    df = pd.read_csv(
        "2022_LoL_esports_match_data_from_OraclesElixir_20221120.csv")
    # Filter by games that are from the world championship
    worlds_games = df[(df['league'] == "WCS")]
    # Filter rows that show individual player data
    individual_stats = worlds_games[(worlds_games['position'] != "team")]
    # Filter rows that show cumulative team data
    game_end_stats = worlds_games[(worlds_games['position'] == "team")]
    # get the total amount of games at worlds
    total_games_at_worlds = total_games(game_end_stats)
    # Get the pick rates for a champion
    pick_rates = pick_rate_func(individual_stats, total_games_at_worlds)
    # Get the ban rates for a champion
    ban_rates = ban_rate_func(game_end_stats, total_games_at_worlds)
    # Get the win rates for a champion
    win_rates = win_rate_func(individual_stats)
    # Combine them all together
    pick_ban_win_rates = pick_ban_win_rates_func(pick_rates,
                                                 ban_rates,
                                                 win_rates)
    # plot the pick, ban and win rates
    plot_pick_ban_wins(pick_ban_win_rates)
    # Plots and model for player named Zeka
    player_name = "Zeka"
    # call to get the amount of games played per champions by Zeka
    plot_champs_at_worlds(player_name, individual_stats)
    # Get the accuracy score for the model for zeka
    print("Accuracy score for", player_name, "is :",
          player_champ_prob_model(player_name, df))
    # Get the accuracy score for the model for Larssen
    player_name = "Larssen"
    print("Accuracy score for", player_name, "is :",
          player_champ_prob_model(player_name, df))
    # Run the model on all players that were at worlds
    # Get the list of the accuracy score for all the models
    model_scores = list_of_model_scores(individual_stats, df)
    # Print the average accuracy score
    print("Average Model Score:", sum(model_scores) / len(model_scores))
    # Get the lowest accuracy score
    print("Min Model Score: ", min(model_scores))
    # Get the highest accuracy score
    print("Max Model Scores: ", max(model_scores))
    # Get the model
    logreg_stats = pob_of_win_total_gold(df)
    # Team Names
    team1 = 'T1'
    team2 = 'JD Gaming'
    team3 = 'Cloud9'
    # Call for T1 and DRX
    predict_win_teams(df, team1, team2, logreg_stats)
    # Call for T1 and Cloud 9
    predict_win_teams(df, team1, team3, logreg_stats)


if __name__ == "__main__":
    main()
