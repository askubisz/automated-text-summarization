# ADDING IMPORTANT MODULES TO MAKE PROGRAM WORK
import bs4 as bs
import urllib.request
import re
import nltk
from urllib import request
from tkinter import *
from stop_words import get_stop_words
from urllib.parse import quote
from deep_translator import GoogleTranslator
from langdetect import detect
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# INITIALIZE INTERPETER FOR TRANSLATOR AND OUR INTERFACE

root=Tk()
root.title("TEXT SUMMARIZATION")

# DEFINING AN ACTUAL FUNCTION THAT SUMMARIZES URL
def summarization_from_url(response,x,y):
    
    # EXTRACTING RAW TEXT FROM SPECIFIC URL AND CREATING VARIABLE TO STORE ALL THE CONTENT
    scraped_data = request.urlopen(response).read().decode('utf8')
    article = scraped_data
    parsed_article = bs.BeautifulSoup(article,'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:
        article_text += p.text

    
    # INITIAL PREPROCESSING. FORMATTING TEXT TO REMOVE IRRELEVANT CHARACTERS
    formatted_article_text = re.sub('[!@#$%^&*]g', ' ', article_text)
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    sentence_list=nltk.tokenize.sent_tokenize(formatted_article_text)
    # TRANSLATING OUR FORMATTED ARTICLE
    translated_formatted_article=GoogleTranslator(source='auto', target='english').translate_batch(sentence_list)
    translated_formatted_article = ' '.join(translated_formatted_article)
   
    # LANGUAGE DETECTION
    lang = detect(formatted_article_text)
    if lang == 'ar':
        lang = 'arabic'
    if lang == 'en':
        lang = 'english'
    if lang == 'es':
        lang = 'spanish'
    if lang == 'de':
        lang = 'german'
    if lang == 'fr':
        lang = 'french'
    if lang == 'zh-cn':
        lang = 'chinese'
    if lang == 'pl':
        lang = 'polish'
    if lang == 'pt':
        lang = 'portuguese'
    
    # SPLITTING FORMATTED TEXT INTO SENTENCES AND GETTING STOPWORDS FOR SPECIFIC LANGUAGE
    
    #nltk.download('punkt')
    #nltk.download('stopwords')
    stopwords = get_stop_words(lang)
    
    
    # FINDING WEIGHTED FREQUENCY OF EACH WORD
    
    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequency = max(word_frequencies.values())
    
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

   
    # CALCULATING SENTECE SCORES
    
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < x:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    
    
    # CREATING SUMMARY FROM TOP Y SENTENCES WITH HIGHEST SCORE
    import heapq
    threshold = y
    summary_sentences = heapq.nlargest(threshold, sentence_scores, key=sentence_scores.get)
    
    # MERGING SENTENCES INTO ONE SUMMARY
    summary = ' '.join(summary_sentences)
    
    # TRANSLATING SUMMARY
    translated_summary=GoogleTranslator(source='auto', target='english').translate_batch(summary_sentences)
    translated_summary = ' '.join(translated_summary)
    
    # WRITING SUMMARY AND TRANSLATED SUMMARY INTO TEXT FILE
    f=open("summary.txt","w",encoding="utf8")
    f.write("Language of article: "+lang+"\n"+"\n"+"Summary:"+"\n"+summary+"\n"+"\n")
    if lang !="english":
        f.write("Translated summary: "+"\n"+translated_summary+"\n"+"\n")
    f.write("Entire article:"+"\n"+formatted_article_text+"\n"+"\n")
    if lang !="english":
        f.write("Translated article: "+"\n"+translated_formatted_article)
    f.close()


    # CREATING WORD CLOUD FOR SUMMARY
    wordcloud_summary = WordCloud(max_font_size=50, max_words=50, background_color="white",width=400,height=400,relative_scaling=1,prefer_horizontal=1,scale=10).generate(translated_summary)

    # CREATING WORD CLOUD FOR WHOLE ARTICLE
    wordcloud_article = WordCloud(max_font_size=50, max_words=50, background_color="white",width=400,height=400,relative_scaling=1,prefer_horizontal=1,scale=10).generate(translated_formatted_article)


    return lang,summary,translated_summary,formatted_article_text,translated_formatted_article,wordcloud_summary,wordcloud_article


# DEFINING ANOTHER FUNCTION TO SUMMARIZE TEXT THAT HAS BEEN PUT INSIDE TEXTBOX. WE USE SAME TECHNIQUES AS IN PREVIOUS FUNCTION
def summarization_from_text(text,x,y):
   
    sentence_list=nltk.tokenize.sent_tokenize(text)
    # TRANSLATING OUR FORMATTED ARTICLE
    translated_text=GoogleTranslator(source='auto', target='english').translate_batch(sentence_list)
    translated_text = ' '.join(translated_text)
    

    lang = detect(text)
    if lang == 'ar':
        lang = 'arabic'
    if lang == 'en':
        lang = 'english'
    if lang == 'es':
        lang = 'spanish'
    if lang == 'de':
        lang = 'german'
    if lang == 'fr':
        lang = 'french'
    if lang == 'zh-cn':
        lang = 'chinese'
    if lang == 'pl':
        lang = 'polish'
    if lang == 'pt':
        lang = 'portugese'
    
    
    #nltk.download('punkt')
    #nltk.download('stopwords')
    stopwords = get_stop_words(lang)
   
    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    
    
    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < x:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]
    

    import heapq
    threshold = y
    summary_sentences = heapq.nlargest(threshold, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summary_sentences)
    
    
    translated_summary=GoogleTranslator(source='auto', target='english').translate_batch(summary_sentences)
    translated_summary = ' '.join(translated_summary)
    
    
    f=open("summary.txt","w",encoding="utf8")
    f.write("Language of article: "+lang+"\n"+"\n"+"Summary:"+"\n"+summary+"\n"+"\n")
    if lang !="english":
        f.write("Translated summary: "+"\n"+translated_summary+"\n"+"\n")
    f.write("Entire article:"+"\n"+text+"\n"+"\n")
    if lang !="english":
        f.write("Translated article: "+"\n"+translated_text)
    f.close()


    wordcloud_summary = WordCloud(max_font_size=50, max_words=50, background_color="white",width=400,height=400,relative_scaling=1,prefer_horizontal=1,scale=10).generate(translated_summary)
   
   
    wordcloud_article = WordCloud(max_font_size=50, max_words=50, background_color="white",width=400,height=400,relative_scaling=1,prefer_horizontal=1,scale=10).generate(translated_text)


    return lang,summary,translated_summary,text,translated_text,wordcloud_summary,wordcloud_article


# MAKING GUI INTERFACE

# CREATING LABEL WITH TEXT AND PLACING IT IN SPECIFIC PLACE
welcome_label=Label(root,text="Input URL here or copy your text into textbox:")
welcome_label.grid(row=0,column=1,columnspan=2)

# CREATING PLACE TO PUT URL
url=Entry(root,width=80)
url.grid(row=1,column=1,columnspan=2)

# CREATING INFORMATION ABOUT FIRST SLIDER 
words_label=Label(root,text="Maximum Number of Words in Sentence:")
words_label.grid(row=0,column=0)

# CREATING INFORMATION ABOUT SECOND SLIDER
sentences_label=Label(root,text="Number of Sentences:")
sentences_label.grid(row=0,column=3)

# CREATING FIRST SLIDER TO ADJUST LENGTH OF SUMMARY
first_entry=Scale(root,from_=1,to=100,orient=HORIZONTAL)
first_entry.set(25)
first_entry.grid(row=1,column=0)

# CREATING SECOND SLIDER TO ADJUST LENGTH OF SUMMARY
second_entry=Scale(root,from_=1,to=50,orient=HORIZONTAL)
second_entry.set(10)
second_entry.grid(row=1,column=3)

# CREATING VARIABLE THAT WILL STORE LANGUAGE OF AN ARTICLE
language=StringVar()
language.set("Language of Article: ") 
language_label=Label(root,textvariable=language)
language_label.grid(row=4,column=1,columnspan=2)

# CREATING VARIABLE THAT WILL STORE URL 
link=StringVar()
link.set("(here you will see if URL loading was successful)")
link_label=Label(root,textvariable=link)
link_label.grid(row=3,column=1,columnspan=2)

# CREATING VARIABLE THAT WILL SHOW IF EDITING INSIDE TEXTBOX IS ENABLED OR NOT
editing_var=StringVar()
editing_var.set("Enabled")
editing_label=Label(root,textvariable=editing_var,fg="green")
editing_label.grid(row=3,column=3)

# CREATING TEXTBOX
original=Text(root,width=150,height=30,wrap=WORD)
original.config(state="normal")
original.grid(row=5,column=0, columnspan=4)


# CREATING FUNCTIONS THAT WILL BE USED FOR BUTTONS LATER ON

# CREATING FUNCTION THAT WILL SUMMARIZE FROM URL
def summary_url():
    link.set("URL loading: Unsuccesful")
    link_label.config(fg="red")
    global result
    result=summarization_from_url(url.get(),first_entry.get(),second_entry.get())
    link.set("URL loading: Succesful")
    link_label.config(fg="green")
    language.set("Language of Article: "+result[0])
    original.config(state="normal")
    original.delete('1.0',END)
    original.config(state="disabled")
    editing_var.set("Disabled")
    editing_label.config(fg="red")

# CREATING FUNCTION THAT WILL SUMMARIZE OUR TEXT IN TEXTBOX
def summary_text():
    global result
    result=summarization_from_text(original.get("1.0","end"),first_entry.get(),second_entry.get())
    link.set("Summarization of specific text")
    link_label.config(fg="black")
    language.set("Language of Article: "+result[0])
    original.config(state="normal")
    original.delete('1.0',END)
    original.config(state="disabled")
    editing_var.set("Disabled")
    editing_label.config(fg="red")

# CREATING FUNCTION THAT WILL SHOW SUMMARY IN ORIGINAL LANGUAGE
def summarize_button():
    original.config(state="normal")
    original.delete('1.0',END) 
    original.insert(INSERT, result[1])
    original.config(state="disabled")
    editing_var.set("Disabled")
    editing_label.config(fg="red")

# CREATING FUNCTION THAT WILL SHOW ENTIRE ARTICLE
def show_article():
    original.config(state="normal")
    original.delete('1.0',END) 
    original.insert(INSERT, result[3])
    original.config(state="disabled")
    editing_var.set("Disabled")
    editing_label.config(fg="red")

# CREATING FUNCTION THAT WILL SHOW ENTIRE TRANSLATED ARTICLE
def show_translated_article():
    original.config(state="normal")
    original.delete('1.0',END) 
    original.insert(INSERT, result[4])
    original.config(state="disabled")
    editing_var.set("Disabled")
    editing_label.config(fg="red")

# CREATING FUNCTION THAT WILL SHOW TRANSLATED SUMMARY
def show_translated_summary():
    original.config(state="normal")
    original.delete('1.0',END) 
    original.insert(INSERT, result[2])
    original.config(state="disabled")
    editing_var.set("Disabled")
    editing_label.config(fg="red")

# CREATING FUNCTION THAT WILL SWITCH BETWEEN BEING ABLE TO EDIT TEXT INSIDE TEXTBOX
def editing():
    if original.config("state")[-1]=="normal":
        original.config(state="disabled")
        editing_var.set("Disabled")
        editing_label.config(fg="red")
    else:
        original.config(state="normal")
        editing_var.set("Enabled")
        editing_label.config(fg="green")

# CREATING FUNCTION TO SHOW WORD CLOUD FROM SUMMARY
def wrdcloud_summary():
    plt.figure(figsize=(7,7))
    plt.imshow(result[5])
    plt.axis("off")
    plt.savefig("word_cloud_summary.png", bbox_inches='tight')
    plt.gcf().canvas.draw()
    plt.show()
    plt.close()

# CREATING FUNCTION TO SHOW WORD CLOUD FROM ARTICLE
def wrdcloud_article():
    plt.figure(figsize=(7,7))
    plt.imshow(result[6])
    plt.axis("off")
    plt.savefig("word_cloud_article.png", bbox_inches='tight')
    plt.gcf().canvas.draw()
    plt.show()
    plt.close()

# CREATING BUTTONS

# CREATING BUTTON FOR SUMMARIZING FROM URL
summary_url_button=Button(text="Summarize from URL",command=summary_url)
summary_url_button.grid(row=2,column=1)

# CREATING BUTTON FOR SUMMARIZING FROM TEXTBOX
summary_text_button=Button(text="Summarize text in textbox",command=summary_text)
summary_text_button.grid(row=2,column=2)

# CREATING BUTTON FOR SWITCHING BETWEEN BEING ABLE TO EDIT TEXT IN TEXTBOX
editing_button=Button(text="Switch editing",command=editing)
editing_button.grid(row=4,column=3)

# CREATING BUTTON TO SHOW SUMMARY IN ORIGINAL LANGUAGE
myButton=Button(root, text="Summarization in Original Language",command=summarize_button)
myButton.grid(row=6,column=0)

# CREATING BUTTON TO SHOW ENTIRE ARTICLE
show_article_button=Button(root, text="Entire Article",command=show_article)
show_article_button.grid(row=6,column=2)

# CREATING BUTTON TO SHOW ENTIRE TRANSLATED ARTICLE
show_translated_article_button=Button(root, text="Entire Translated Article",command=show_translated_article)
show_translated_article_button.grid(row=6,column=3)

# CREATING BUTTON TO SHOW TRANSLATED SUMMARIZATION
show_translated_summarization=Button(root, text="Translated Summarization",command=show_translated_summary)
show_translated_summarization.grid(row=6,column=1)

# CREATING BUTTON TO SHOW WORD CLOUD FROM SUMMARY
show_wordcloud_summary=Button(root, text="Show wordcloud from summary", command=wrdcloud_summary)
show_wordcloud_summary.grid(row=4,column=0)

# CREATING BUTTON TO SHOW WORD CLOUD FROM ARTICLE
show_wordcloud_article=Button(root, text="Show wordcloud from article", command=wrdcloud_article)
show_wordcloud_article.grid(row=3,column=0)


root.mainloop()
