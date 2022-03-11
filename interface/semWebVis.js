
let node_list = [];
let edge_list = [];
let space = 0;

class node
{
  constructor(x,y,t,h)
  {
    this.x = ((y)*20)+10;
    this.y = ((x)*20)+10;
    this.text_value = t;
    this.hash_value = h;
    this.diameter = 20;
  }
  display()
  {
    ellipse(this.x, this.y, this.diameter, this.diameter);
    text(this.text_value, this.x, this.y);
  }
}

class edge
{
  constructor(x,y,x2,y2)
  {
    this.startx = ((x)*20)+10;
    this.starty = ((y)*20)+10;
    this.endx = ((x2)*20)+10;
    this.endy = ((y2)*20)+10;
  }
  display()
  {
    stroke(153);
    line(this.startx,this.starty,this.endx,this.endy);
  }
}

let font,fontsize = 8;
function preload() {
  font = loadFont('assets/SourceSansPro-Light.ttf');
  prison = loadJSON("assets/imprisoned_web.json");
}

function setup()
{
  var x = 0;
  var y = 0;
  var text = '';
  var hash = '';
  var coords = [];
  var ncounter=0;
  var ecounter=0;
  for(key in prison)
  {
    if(key.includes("-"))
    {
      coords = key.split("-");
      x = parseInt(coords[0]);
      y =  parseInt(coords[1]);
      text = prison[key]['text'];
      hash = prison[key]['hash'];
      node_list[ncounter] = new node(x,y,text,hash)
      ncounter = ncounter+1;
    }
  }
  var s_coords = "";
  var e_coords = "";
  for(key in prison["edges"])
  {

    s_coords = prison["edges"][key]['startkey'].split("-");
    e_coords = prison["edges"][key]['endkey'].split("-");
    edge_list[ecounter] = new edge(parseInt(s_coords[0]),parseInt(s_coords[1]),parseInt(e_coords[0]),parseInt(e_coords[1]))
    ecounter= ecounter+1;
  }

  createCanvas(8192, 8192);
  textFont(font);
  textSize(fontsize);
  textAlign(CENTER, CENTER);
  console.log(edge_list);
}

function draw()
{
  background(220);
  for(let i = 0; i < edge_list.length; i++)
  {
    edge_list[i].display();
  }
  for (let i = 0; i < node_list.length; i++)
  {
    node_list[i].display();
  }

}
