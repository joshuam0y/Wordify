"""
wordify.py: An extensive framework for comparative text analysis
Author: Joshua Moy
"""

from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import string
import seaborn as sns

class Wordify:
    def __init__(self):
        """ Constructor to initialize state """
        self.data = defaultdict(dict)
        self.stop_words = set()

    def load_stop_words(self, stopfile):
        """ Load common stop words from a file """
        try:
            with open(stopfile, 'r', encoding='utf-8') as f:
                self.stop_words = set(word.strip().lower() for word in f.readlines())
            print(f"Loaded {len(self.stop_words)} stop words")
        except FileNotFoundError:
            print(f"Warning: {stopfile} not found.")
            self.stop_words = set()

    @staticmethod
    def default_parser(filename):
        """ For processing plain text ascii files (.txt) """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
            text_clean = text.lower()
            text_clean = text_clean.translate(str.maketrans('', '', string.punctuation))
            words = text_clean.split()
            wordcount = Counter(words)
            numwords = len(words)
            results = {
                'wordcount': wordcount,
                'numwords': numwords,
                'raw_text': text
            }
            print(f"Parsed {filename}: {numwords} words")
            return results
        except FileNotFoundError:
            print(f"Error: {filename} not found")
            return {'wordcount': Counter(), 'numwords': 0, 'raw_text': ''}

    def load_text(self, filename, label=None, parser=None):
        """ Register a text document with the framework """
        if parser is None:
            results = Wordify.default_parser(filename)
        else:
            results = parser(filename)
        if label is None:
            label = filename
        if 'wordcount' in results and self.stop_words:
            filtered_wordcount = Counter()
            for word, count in results['wordcount'].items():
                if word not in self.stop_words and len(word) > 1:
                    filtered_wordcount[word] = count
            results['wordcount'] = filtered_wordcount
        for k, v in results.items():
            self.data[k][label] = v

    def wordcount_sankey(self, word_list=None, k=5):
        """
        Sankey diagram mapping texts to their most common words
        """
        if word_list is None:
            all_words = set()
            for label, wordcount in self.data['wordcount'].items():
                top_k = [word for word, count in wordcount.most_common(k)]
                all_words.update(top_k)
            word_list = list(all_words)

        sources = []
        targets = []
        values = []

        text_labels = list(self.data['wordcount'].keys())
        all_labels = text_labels + word_list
        label_to_idx = {label: idx for idx, label in enumerate(all_labels)}

        for text_label, wordcount in self.data['wordcount'].items():
            text_idx = label_to_idx[text_label]
            for word in word_list:
                if word in wordcount:
                    count = wordcount[word]
                    if count > 0:
                        sources.append(text_idx)
                        targets.append(label_to_idx[word])
                        values.append(count)

        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,
                thickness=25,
                line=dict(color="black", width=1),
                label=all_labels,
                color="lightblue"
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                color="rgba(0,0,255,0.2)"
            )
        )])

        fig.update_layout(
            title_text="Document to Word Sankey Diagram",  # GENERIC
            title_font_size=20,
            font_size=14,
            height=500,
            width=1000,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        fig.write_html("sankey_diagram.html")
        fig.show()

    def word_frequency_heatmap(self, top_n=10):
        """
        Heatmap showing word frequencies across different texts
        """
        # Get top N words
        all_word_counts = Counter()
        for wordcount in self.data['wordcount'].values():
            all_word_counts.update(wordcount)
        top_words = [word for word, count in all_word_counts.most_common(top_n)]
        text_labels = list(self.data['wordcount'].keys())
        freq_matrix = []

        for label in text_labels:
            wordcount = self.data['wordcount'][label]
            row = [wordcount.get(word, 0) for word in top_words]
            freq_matrix.append(row)

        fig, ax = plt.subplots(figsize=(14, 10))
        sns.heatmap(
            freq_matrix,
            annot=False,
            fmt='d',
            cmap='viridis',
            xticklabels=top_words,
            yticklabels=text_labels,
            cbar_kws={'label': 'Word Frequency'},
            linewidths=0.5,
            ax=ax
        )
        ax.set_title(f'Word Frequency Heatmap: Top {top_n} Words',
                     fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Words', fontsize=12, fontweight='bold')
        ax.set_ylabel('Documents', fontsize=12, fontweight='bold')

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('word_frequency_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()

    def comparative_word_graph(self, top_n=15, rotation=45):
        """
        Subplots comparing word frequency across documents.
        Fixes x-label cutoff by rotating labels only on the bottom subplot
        and increasing the bottom margin dynamically.
        """
        from collections import Counter

        # Collect top N most common words across all documents
        all_word_counts = Counter()
        for wc in self.data['wordcount'].values():
            all_word_counts.update(wc)
        common_words = [w for w, _ in all_word_counts.most_common(top_n)]

        labels = list(self.data['wordcount'].keys())
        num_docs = len(labels)

        fig, axes = plt.subplots(num_docs, 1, figsize=(16, 3.5 * num_docs), sharex=True)

        if num_docs == 1:
            axes = [axes]

        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#ffa07a',
                  '#98d8c8', '#f7dc6f', '#bb8fce', '#85c1e9']

        for idx, (label, wordcount) in enumerate(self.data['wordcount'].items()):
            ax = axes[idx]
            freqs = [wordcount.get(word, 0) for word in common_words]
            ax.plot(common_words, freqs,
                    marker='o', linewidth=2.5, markersize=7,
                    color=colors[idx % len(colors)], alpha=0.85)
            ax.set_title(f'{label} — Top {top_n} Words', fontsize=13, fontweight='bold', pad=8)
            ax.set_ylabel('Freq', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.25, linestyle='--')

            if idx != num_docs - 1:
                ax.set_xticklabels([])

        bottom_ax = axes[-1]
        bottom_ax.set_xlabel('Words', fontsize=12, fontweight='bold')
        bottom_ax.set_xticks(range(len(common_words)))
        bottom_ax.set_xticklabels(common_words, rotation=rotation, ha='right', fontsize=11)

        max_label_len = max((len(w) for w in common_words), default=0)
        bottom_margin = min(0.5, 0.12 + 0.008 * max_label_len + (0.08 if rotation >= 60 else 0.0))

        fig.subplots_adjust(hspace=0.45, bottom=bottom_margin, top=0.95)
        plt.tight_layout(rect=(0, bottom_margin, 1, 0.98))
        plt.savefig("comparative_word_usage_subplots.png", dpi=300, bbox_inches='tight')
        plt.show()

