from bokeh.plotting import output_notebook, figure, show
from bokeh.models import HoverTool

output_notebook()

x = list(range(10))
y1 = [3,5,3,2,6,7,4,3,6,5]
y2 = [2,5,4,6,4,3,6,4,3,2]
y3 = [5,3,8,5,3,7,5,3,8,5]

hover = HoverTool(names=["foo", "bar"])

p = figure(plot_width=600, plot_height=300, tools=[hover,])
p.circle(x, y1, size=10, name="foo", color='red')
p.square(x, y2, size=10, name="bar", color='blue')
p.line(x=x, y=y3, color='black')
show(p)