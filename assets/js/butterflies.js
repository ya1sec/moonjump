document.addEventListener("DOMContentLoaded", function (event) {
  const Settings = {
    url: window.location.hostname,
  };

  function shuffle(array) {
    var currentIndex = array.length,
      temporaryValue,
      randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {
      // Pick a remaining element...
      randomIndex = Math.floor(Math.random() * currentIndex);
      currentIndex -= 1;

      // And swap it with the current element.
      temporaryValue = array[currentIndex];
      array[currentIndex] = array[randomIndex];
      array[randomIndex] = temporaryValue;
    }

    return array;
  }

  function random(min, max) {
    return Math.floor(Math.random() * (max - min + 1) + min);
  }

  const helpers = {
    init: function () {
      helpers.checkLinks();
    },

    checkLinks: function () {
      var links = document.getElementsByTagName("a");
      for (var i = 0; i < links.length; i++) {
        href = links[i].getAttribute("href");

        if (href === null) {
          return;
        } else if (href.startsWith("/")) {
          links[i].setAttribute("target", "_self");
        } else if (href.includes(Settings.url)) {
          links[i].setAttribute("target", "_self");
        } else if (href.startsWith("http://")) {
          links[i].setAttribute("target", "_blank");
        } else if (href.startsWith("https://")) {
          links[i].setAttribute("target", "_blank");
        } else if (href.startsWith("mailto")) {
          links[i].setAttribute("target", "_blank");
        } else if (href.startsWith("#")) {
          links[i].setAttribute("target", "_self");
        }
      }
    },
  };
  let butterflyCount = 2;
  let butterflies = [
    {
      id: "red-black",
      wingleft: "assets/media/butterfly/red-black/left.png",
      wingright: "assets/media/butterfly/red-black/right.png",
      size: 32,
      flyspeed: 40,
      flapspeed: 0.444,
    },

    {
      id: "xray",
      wingleft: "assets/media/butterfly/xray/left.png",
      wingright: "assets/media/butterfly/xray/right.png",
      size: 40,
      flyspeed: 40,
      flapspeed: 0.333,
    },
  ];

  const world = {
    width: window.innerWidth,
    height: window.innerHeight,
    // windspeed: 4.1,
    windspeedX: random(-1, 1),
    windspeedY: random(-1, 1),
    wihdirection: 90, // in degrees 0 = N, E = 90, W = 270

    bloom: function () {
      world.shuffleButterflies();
      world.flower();
    },

    shuffleButterflies: function () {
      butterflies = shuffle(butterflies);
    },

    flower: function () {
      var index = 0;
      butterflies.forEach(function (params) {
        index++;
        if (index <= butterflyCount) {
          new butterfly(params);
        }
      });
    },
  };

  class butterfly {
    constructor(params) {
      this.id = params.id;
      this.wing = params.wing;
      this.wingleft = params.wingleft;
      this.wingright = params.wingright;
      this.size = params.size;
      this.flapspeed = params.flapspeed;
      this.flyspeed = params.flyspeed;
      this.posX = world.width * random(-1, 2);
      this.posY = world.height * random(-1, 2);
      this.a = 0; // in radian
      this.r = random(50, 100);
      this.da = this.r / 2000;
      this.x = 0;
      this.y = 0;
      this.rotation = 0;
      this.rotationSpeed = random(0.2, 2);
      this.rotationMax = random(20, 60);
      this.rotationMin = this.rotationMax * -1;
      this.rotationDirection = "clockwise";
      this.positionTransform = "";
      this.rotationTransform = "";
      this.windspeedX = random(-1, 1);
      this.windspeedY = random(-1, 1);

      var self = this;
      // console.log(self);
      this.makeElement(self);

      setInterval(function () {
        self.rotating(self);
        self.movePos(self);
        self.moveCirclular(self);
        self.allTogether(self);
      }, 40);
    }

    makeElement(params) {
      var butterflyEl = document.createElement("butterfly");
      butterflyEl.setAttribute("data-id", params.id);
      butterflyEl.setAttribute("data-hidden", "true");
      butterflyEl.style.width = params.size + "px";
      butterflyEl.style.height = params.size + "px";
      // butterflyEl.style.left = params.posX + 'px';
      // butterflyEl.style.top = params.posY + 'px';
      document.body.appendChild(butterflyEl);
      params.el = butterflyEl;

      var butterflyWingLeft = document.createElement("wing");
      butterflyWingLeft.setAttribute("data-side", "left");
      butterflyWingLeft.style.backgroundImage = "url(" + params.wingleft + ")";
      butterflyWingLeft.style.animationDuration = params.flapspeed + "s";
      butterflyEl.appendChild(butterflyWingLeft);

      var butterflyWingRight = document.createElement("wing");
      butterflyWingRight.setAttribute("data-side", "right");
      butterflyWingRight.style.animationDuration = params.flapspeed + "s";
      butterflyWingRight.style.backgroundImage =
        "url(" + params.wingright + ")";
      butterflyEl.appendChild(butterflyWingRight);
    }

    rotating(params) {
      if (params.rotationDirection === "clockwise") {
        params.rotation = params.rotation + params.rotationSpeed;
      }
      if (params.rotationDirection === "counter") {
        params.rotation = params.rotation - params.rotationSpeed;
      }
      if (params.rotation > params.rotationMax) {
        params.rotationDirection = "counter";
        params.rotationMax = random(-60, 20);
        params.rotationSpeed = random(0.2, 2);
        params.windspeedX = random(-1, 1);
        params.windspeedY = random(-1, 1);
      }
      if (params.rotation < params.rotationMin) {
        params.rotationDirection = "clockwise";
        params.rotationMax = random(20, 60);
        params.rotationSpeed = random(0.2, 2);
        params.windspeedX = random(-1, 1);
        params.windspeedY = random(-1, 1);
      }
      var rotationTransform = "rotate(" + params.rotation + "deg)";
      params.rotationTransform = rotationTransform;
    }

    movePos(params) {
      params.posX = params.posX + params.windspeedX;
      params.posY = params.posY + params.windspeedY;

      if (params.posX > world.width + 200) {
        params.posX = -200;
      }
      if (params.posX < -200) {
        params.posX = world.width + 200;
      }
      if (params.posY > world.height + 200) {
        params.posY = -200;
      }
      if (params.posY < -200) {
        params.posY = world.height + 200;
      }
    }

    moveCirclular(params) {
      params.a += params.da;
      params.x = params.posX + params.r * Math.sin(params.a);
      params.y = params.posY + params.r * Math.cos(params.a);
      params.positionTransform =
        "translate3d(" + params.x + "px, " + params.y + "px, 0)";
    }

    allTogether(params) {
      params.el.style.transform =
        params.positionTransform + " " + params.rotationTransform;
      params.el.style.zIndex = 1000;
      params.el.setAttribute("data-hidden", "false");
    }
  }

  world.bloom();
  helpers.init();
});
