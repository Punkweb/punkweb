(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = Object.setPrototypeOf ||
        ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
        function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
var squire_1 = require("./squire");
var ShietyShooter = (function (_super) {
    __extends(ShietyShooter, _super);
    function ShietyShooter() {
        var _this = _super.call(this, 'shietyshooter') || this;
        _this.gameState = new GameState(_this);
        _this.stateManager.state = _this.gameState;
        return _this;
    }
    return ShietyShooter;
}(squire_1.SquireGame));
exports.ShietyShooter = ShietyShooter;
var GameState = (function (_super) {
    __extends(GameState, _super);
    function GameState(gameCtx) {
        var _this = _super.call(this, gameCtx) || this;
        _this.started = false;
        _this.characterSprite1 = null;
        _this.characterSprite2 = null;
        _this.grassSprite = null;
        _this.dirtSprite = null;
        _this.song = null;
        _this.health = 100;
        _this.reloadTime = 40;
        _this.enemyDamage = 5;
        _this.playerMaxDamage = 40;
        _this.playerMinDamage = 20;
        _this.ownProjectiles = [];
        _this.enemyProjectiles = [];
        _this.enemies = [];
        _this.characterSprite1 = new Image();
        _this.characterSprite1.onload = function () { };
        _this.characterSprite1.src = 'https://punkweb.net/static/punkweb/js/assets/character-right.png';
        _this.characterSprite2 = new Image();
        _this.characterSprite2.onload = function () {
            console.log('Image loaded: ' + 'https://punkweb.net/static/punkweb/js/assets/character-left.png');
        };
        _this.characterSprite2.src = 'https://punkweb.net/static/punkweb/js/assets/character-left.png';
        _this.grassSprite = new Image();
        _this.grassSprite.onload = function () {
            console.log('Image loaded: ' + 'https://punkweb.net/static/punkweb/js/assets/grass.png');
        };
        _this.grassSprite.src = 'https://punkweb.net/static/punkweb/js/assets/grass.png';
        _this.dirtSprite = new Image();
        _this.dirtSprite.onload = function () {
            console.log('Image loaded: ' + 'https://punkweb.net/static/punkweb/js/assets/dirt.png');
        };
        _this.dirtSprite.src = 'https://punkweb.net/static/punkweb/js/assets/dirt.png';
        _this.song = new Audio('https://punkweb.net/static/punkweb/js/assets/Shiety_Blues-JackStraw.mp3');
        _this.song.loop = true;
        _this.song.currentTime = 0;
        _this.gameCtx.canvas.addEventListener('click', _this.onClick.bind(_this), false);
        return _this;
    }
    GameState.prototype.onClick = function (canvasEvent) {
        var offsetX, offsetY = 0;
        var element = this.gameCtx.canvas;
        offsetX = this.gameCtx.canvas.offsetLeft;
        offsetY = this.gameCtx.canvas.offsetTop;
        var actualClickX = canvasEvent.clientX - offsetX;
        var actualClickY = canvasEvent.clientY - offsetY;
        if (this.started) {
            this.ownProjectiles.push({
                x: 200,
                y: 600 - 128 - 120
            });
        }
        else {
            this.health = 100;
            this.ownProjectiles = [];
            this.enemyProjectiles = [];
            this.enemies = [];
            this.started = true;
            this.song.play();
        }
    };
    GameState.prototype.init = function () { };
    GameState.prototype.end = function () { };
    GameState.prototype.render = function (r) {
        var _this = this;
        r.rect('#7EC0EE', 0, 0, 1024, 600);
        if (!this.started) {
            r.text('Click to start', 12, 160, 'black', '72px Verdana');
            return;
        }
        if (this.grassSprite) {
            for (var i = 0; i < 1024; i += 128) {
                var dx = i;
                var dy = 600 - 128;
                r.image(this.grassSprite, 0, 0, 128, 128, dx, dy, 128, 128);
            }
        }
        if (this.characterSprite1) {
            var dy = 600 - 128 - 203;
            r.image(this.characterSprite1, 0, 0, 161, 203, 40, dy, 161, 203);
        }
        if (this.enemies && this.characterSprite2) {
            this.enemies.forEach(function (obj) {
                var dy = 600 - 128 - 203;
                r.image(_this.characterSprite2, 0, 0, 161, 203, obj.x, dy, 161, 203);
                var percentHealth = obj.health / 100;
                r.rect('#282828', obj.x + 80, dy - 40, 104, 12);
                r.rect('red', obj.x + 82, dy - 38, 100 * percentHealth, 8);
            });
        }
        if (this.ownProjectiles) {
            this.ownProjectiles.forEach(function (obj) {
                r.circle('red', obj.x, obj.y, 2);
            });
        }
        if (this.enemyProjectiles) {
            this.enemyProjectiles.forEach(function (obj) {
                r.circle('red', obj.x, obj.y, 2);
            });
        }
        var percentHealth = this.health / 100;
        r.rect('#282828', 12, 12, 240, 24);
        r.rect('red', 14, 14, 236 * percentHealth, 20);
    };
    GameState.prototype.update = function (dt) {
        var _this = this;
        if (!this.started) {
            return;
        }
        if (Math.random() > .99) {
            this.enemies.push({
                x: 1024,
                lastShot: 30,
                health: 100,
            });
        }
        if (this.enemies) {
            this.enemies.forEach(function (obj, i) {
                obj.x -= 5;
                if (obj.x <= -180) {
                    _this.enemies.splice(i, 1);
                }
                obj.lastShot++;
                if (obj.lastShot > 60) {
                    _this.enemyProjectiles.push({
                        x: obj.x,
                        y: 600 - 128 - 120
                    });
                    obj.lastShot = 0;
                }
            });
        }
        this.ownProjectiles.forEach(function (obj, i) {
            obj.x += 15;
            if (obj.x > 1024) {
                _this.ownProjectiles.splice(i, 1);
            }
            if (_this.enemies.length > 0) {
                var firstEnemy = _this.enemies.sort(function (a, b) {
                    return a.x - b.x;
                })[0];
                if (obj.x >= firstEnemy.x) {
                    firstEnemy.health -= ((Math.random() * _this.playerMaxDamage) + _this.playerMinDamage);
                    _this.ownProjectiles.splice(i, 1);
                    if (firstEnemy.health < 1) {
                        var index = _this.enemies.indexOf(firstEnemy);
                        _this.enemies.splice(index, 1);
                    }
                }
            }
        });
        this.enemyProjectiles.forEach(function (obj, i) {
            obj.x -= 15;
            if (obj.x <= 200) {
                _this.health -= _this.enemyDamage;
                _this.enemyProjectiles.splice(i, 1);
                if (_this.health < 1) {
                    _this.started = false;
                    _this.song.currentTime = 0;
                    _this.song.pause();
                }
            }
        });
    };
    return GameState;
}(squire_1.State));
exports.GameState = GameState;
window.onload = function () {
    var shietyshooter = new ShietyShooter();
    shietyshooter.run();
};

},{"./squire":7}],2:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var AnimationDef = (function () {
    function AnimationDef() {
        this.animations = {};
        this.sheet = new Image();
        this.sheet.onload = function () { };
        this.sheet.src = this.getImageUrl();
    }
    AnimationDef.prototype.getImageUrl = function () { return undefined; };
    AnimationDef.prototype.getFrame = function (animationName, frameNumber, direction) {
        var frames = this.animations[animationName]["frames"];
        return frames.find(function (frame) {
            return frame[0] === frameNumber && frame[1] === direction;
        });
    };
    AnimationDef.prototype.render = function (r, animationName, frameNumber, direction, x, y) {
        if (!this.sheet) {
            return;
        }
        var frame = this.getFrame(animationName, frameNumber, direction);
        var sheet_x = frame[2];
        var sheet_y = frame[3];
        var w = frame[4];
        var h = frame[5];
        var offset_x = frame[6];
        var offset_y = frame[7];
        r.image(this.sheet, sheet_x, sheet_y, w, h, x - offset_x, y - offset_y, w, h);
    };
    return AnimationDef;
}());
exports.AnimationDef = AnimationDef;

},{}],3:[function(require,module,exports){
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
__export(require("./iso-helper"));

},{"./iso-helper":4}],4:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var utils_1 = require("../../../utils");
var IsoHelper = (function () {
    function IsoHelper() {
    }
    IsoHelper.isoTo2D = function (pt) {
        var tempPt = new utils_1.Point2d(0, 0);
        tempPt.x = (2 * pt.y + pt.x) / 2;
        tempPt.y = (2 * pt.y - pt.x) / 2;
        return tempPt;
    };
    IsoHelper.twoDToIso = function (pt) {
        var tempPt = new utils_1.Point2d(0, 0);
        tempPt.x = pt.x - pt.y;
        tempPt.y = (pt.x + pt.y) / 2;
        return tempPt;
    };
    IsoHelper.getTileCoordinates = function (pt, tileHeight) {
        var tempPt = new utils_1.Point2d(0, 0);
        tempPt.x = Math.floor(pt.x / tileHeight);
        tempPt.y = Math.floor(pt.y / tileHeight);
        return tempPt;
    };
    IsoHelper.get2dFromTileCoordinates = function (pt, tileHeight) {
        var tempPt = new utils_1.Point2d(0, 0);
        tempPt.x = pt.x * tileHeight;
        tempPt.y = pt.y * tileHeight;
        return tempPt;
    };
    return IsoHelper;
}());
exports.IsoHelper = IsoHelper;

},{"../../../utils":12}],5:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Connection = (function () {
    function Connection(url) {
        this.socket = new WebSocket(url);
    }
    return Connection;
}());
exports.Connection = Connection;

},{}],6:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Event = (function () {
    function Event(zIndex) {
        this.zIndex = zIndex;
    }
    Event.prototype.handleEvent = function (event, stateCtx) { };
    return Event;
}());
exports.Event = Event;

},{}],7:[function(require,module,exports){
"use strict";
function __export(m) {
    for (var p in m) if (!exports.hasOwnProperty(p)) exports[p] = m[p];
}
Object.defineProperty(exports, "__esModule", { value: true });
__export(require("./com/csharks/juwalabose"));
__export(require("./animation"));
__export(require("./connection"));
__export(require("./event"));
__export(require("./renderer"));
__export(require("./squire-game"));
__export(require("./state-manager"));
__export(require("./state"));
__export(require("./utils"));

},{"./animation":2,"./com/csharks/juwalabose":3,"./connection":5,"./event":6,"./renderer":8,"./squire-game":9,"./state":11,"./state-manager":10,"./utils":12}],8:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Renderer = (function () {
    function Renderer(ctx) {
        this.ctx = ctx;
    }
    Renderer.prototype.clear = function (x, y, w, h) {
        this.ctx.clearRect(x, y, w, h);
    };
    Renderer.prototype.rect = function (color, x, y, w, h) {
        this.ctx.fillStyle = color;
        this.ctx.fillRect(x, y, w, h);
    };
    Renderer.prototype.circle = function (color, x, y, radius) {
        this.ctx.beginPath();
        this.ctx.fillStyle = color;
        this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
        this.ctx.fill();
    };
    Renderer.prototype.text = function (text, x, y, color, font) {
        if (color === void 0) { color = 'black'; }
        if (font === void 0) { font = '16px Arial'; }
        this.ctx.fillStyle = color;
        this.ctx.font = font;
        this.ctx.fillText(text, x, y);
    };
    Renderer.prototype.image = function (image, sX, sY, sW, sH, dX, dY, dW, dH) {
        this.ctx.drawImage(image, sX, sY, sW, sH, dX, dY, dW, dH);
    };
    Renderer.prototype.hr = function (x, y, w, color, lineWidth) {
        if (color === void 0) { color = 'black'; }
        if (lineWidth === void 0) { lineWidth = 1; }
        this.ctx.beginPath();
        this.ctx.fillStyle = color;
        this.ctx.lineWidth = lineWidth;
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x + w, y);
        this.ctx.stroke();
    };
    Renderer.prototype.line = function (x1, y1, x2, y2, color, lineWidth) {
        if (color === void 0) { color = 'black'; }
        if (lineWidth === void 0) { lineWidth = 1; }
        this.ctx.beginPath();
        this.ctx.lineWidth = lineWidth;
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
    };
    Renderer.prototype.triangle = function (color, x, y, w, h) {
        this.ctx.beginPath();
        this.ctx.moveTo(x, y);
        this.ctx.lineTo(x + w / 2, y + h);
        this.ctx.lineTo(x - w / 2, y + h);
        this.ctx.closePath();
        this.ctx.fillStyle = color;
        this.ctx.fill();
    };
    return Renderer;
}());
exports.Renderer = Renderer;

},{}],9:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var _1 = require("./");
var SquireGame = (function () {
    function SquireGame(canvasId) {
        this.lastTickTime = Date.now();
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.size = new _1.Dimension2d(this.canvas.width, this.canvas.height);
        this.center = new _1.Point2d(this.size.w / 2, this.size.h / 2);
        this.renderer = new _1.Renderer(this.ctx);
        this.stateManager = new _1.StateManager();
    }
    SquireGame.prototype.run = function () {
        var _this = this;
        requestAnimationFrame(function () {
            _this.run();
        });
        this.renderer.clear(0, 0, this.size.w, this.size.h);
        var now = Date.now();
        var dt = (now - this.lastTickTime) / 1000;
        this.lastTickTime = now;
        this.stateManager.update(dt);
        this.stateManager.render(this.renderer);
    };
    return SquireGame;
}());
exports.SquireGame = SquireGame;

},{"./":7}],10:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var StateManager = (function () {
    function StateManager() {
    }
    StateManager.prototype.update = function (dt) {
        try {
            this.state.update(dt);
        }
        catch (e) {
            console.error(e);
        }
    };
    StateManager.prototype.render = function (r) {
        try {
            this._state.render(r);
        }
        catch (e) {
            console.error(e);
        }
    };
    Object.defineProperty(StateManager.prototype, "state", {
        get: function () {
            return this._state;
        },
        set: function (value) {
            this._state = value;
            this._state.init();
        },
        enumerable: true,
        configurable: true
    });
    return StateManager;
}());
exports.StateManager = StateManager;

},{}],11:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var State = (function () {
    function State(gameCtx) {
        this.gameCtx = gameCtx;
    }
    return State;
}());
exports.State = State;

},{}],12:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Dimension2d = (function () {
    function Dimension2d(w, h) {
        this.w = w;
        this.h = h;
    }
    return Dimension2d;
}());
exports.Dimension2d = Dimension2d;
var Point2d = (function () {
    function Point2d(x, y) {
        this.x = x;
        this.y = y;
    }
    Point2d.prototype.up = function (px) {
        this.y -= px;
    };
    Point2d.prototype.down = function (px) {
        this.y += px;
    };
    Point2d.prototype.left = function (px) {
        this.x -= px;
    };
    Point2d.prototype.right = function (px) {
        this.x += px;
    };
    Point2d.angleBetween = function (pointA, pointB) {
        return Math.atan2(pointB.y - pointA.y, pointB.x - pointA.x) * 180 / Math.PI;
    };
    Point2d.inRange = function (pointA, pointB, range) {
        var targetDx = pointA.x - pointB.x;
        var targetDy = pointA.y - pointB.y;
        var targetWithinX = Math.abs(targetDx) < range;
        var targetWithinY = Math.abs(targetDy) < (range / 2);
        return targetWithinX && targetWithinY;
    };
    return Point2d;
}());
exports.Point2d = Point2d;
var Random = (function () {
    function Random() {
    }
    Random.between = function (min, max) {
        return Math.floor(Math.random() * (max - min)) + Math.floor(min);
    };
    return Random;
}());
exports.Random = Random;

},{}]},{},[1]);
