var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterGameController',
    function ($scope, GameSetting, Player, Game, $timeout) {
        initGame();
        $scope.gametypes = GameSetting.query({settingName: "gametypes"});
        $scope.mapstyles = GameSetting.query({settingName: "mapstyles"});
        $scope.locations = GameSetting.query({settingName: "location"});
        $scope.sizes = GameSetting.query({settingName: "sizes"});
        $scope.resourcesList = GameSetting.query({settingName: "resourceslist"});
        $scope.gameSpeeds = GameSetting.query({settingName: "gamespeeds"});
        $scope.victoryList = GameSetting.query({settingName: "victorylist"});
        $scope.civilizations = GameSetting.query({settingName: "civilizations"});
        $scope.allPlayers = Player.query();

        $scope.submitGame = function () {
            Game.save($scope.game).$promise.then(
                //success
                function (value) {
                    initGame();
                    $scope.error = "";
                    $scope.success = "Game saved";
                    $timeout(function(){
                        $scope.success = "";
                    }, 3000);

                },
                //error
                function (error) {
                    $scope.error = 'Failed to save game. ' + error.data;
                }
            )
        };


        function initGame() {
            $scope.game = new Game();
            $scope.game.playerResults = [];
            $scope.game.gameType = "";
            $scope.game.mapStyle = "";
            $scope.game.location = "";
            $scope.game.size = "";
            $scope.game.resources = "";
            $scope.game.gameSpeed = "";
            $scope.game.victory = "";
            for (i = 0; i < 8; i++) {
                $scope.game.playerResults.push({'playerId': "", 'civilization': "", 'team': 0, 'iswinner': false});
            }
        };
    });


siAgeApp.filter('range', function () {
    return function (input, min, max) {
        min = parseInt(min); //Make string input int
        max = parseInt(max);
        for (var i = min; i < max; i++)
            input.push(i);
        return input;
    }
});
