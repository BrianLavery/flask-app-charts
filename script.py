from flask import Flask, render_template

app = Flask(__name__)

@app.route('/plot')
def plot():
    from pandas_datareader import data
    from datetime import datetime as dt
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start = dt(2015,11,1)
    end = dt(2016,3,10)

    df = data.DataReader(name='GOOG', data_source="yahoo", start=start, end=end)

    def inc_dec(c, o):
        if c > o:
            value = "Increase"
        elif c < o:
            value = "Decrease"
        else:
            value = "Equal"
        return value

    df["Status"] = [inc_dec(c,o) for c, o in zip(df.Close, df.Open)]
    df["Midpoint"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type = 'datetime', width = 1000, height = 300, sizing_mode = "scale_width")
    p.title.text = "Candlestick Chart"
    p.grid.grid_line_alpha = 0.2

    hours_12 = 12 * 60 * 60 * 1000 # 12 hours in milliseconds

    p.segment(df.index, df.High, df.index, df.Low, color="Grey")
    p.rect(df.index[df.Status == "Increase"], df.Midpoint[df.Status == "Increase"], hours_12, df.Height[df.Status == "Increase"], fill_color = "#90EE90", line_color = "grey")
    p.rect(df.index[df.Status == "Decrease"], df.Midpoint[df.Status == "Decrease"], hours_12, df.Height[df.Status == "Decrease"], fill_color = "#FF6347", line_color = "grey")

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]

    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__": 
    app.run(debug = True)

