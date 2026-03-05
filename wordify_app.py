"""
wordify_app.py: Application that runs Wordify
Author: Joshua Moy
"""

from wordify import Wordify

def main():
    tt = Wordify()
    tt.load_stop_words('stopwords.txt')
    tt.load_text('carmelo_anthony.txt', 'Carmelo Anthony')
    tt.load_text('ben_wallace.txt', 'Ben Wallace')
    tt.load_text('sidney_moncrief.txt', 'Sidney Moncrief')
    tt.load_text('tracy_mcgrady.txt', 'Tracy McGrady')
    tt.load_text('jason_kidd.txt', 'Jason Kidd')
    tt.load_text('scottie_pippen.txt', 'Scottie Pippen')
    tt.load_text('kevin_garnett.txt', 'Kevin Garnett')
    tt.load_text('yao_ming.txt', 'Yao Ming')

    # Run the app for Sankey diagram
    tt.wordcount_sankey(k=5)

    # Run the app for a subplots heatmap
    tt.word_frequency_heatmap(top_n=8)

    # Run the app for an overlay comparison
    tt.comparative_word_graph(top_n=10)

if __name__ == "__main__":
    main()
