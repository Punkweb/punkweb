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
        _this.health = 100;
        _this.reloadTime = 40;
        _this.enemyDamage = 5;
        _this.playerMaxDamage = 40;
        _this.playerMinDamage = 20;
        _this.ownProjectiles = [];
        _this.enemyProjectiles = [];
        _this.enemies = [];
        _this.characterSprite1 = new Image();
        _this.characterSprite1.onload = function () {
            console.log('Image loaded: ' + 'https://punkweb.net/static/punkweb/js/assets/character-right.png');
        };
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
