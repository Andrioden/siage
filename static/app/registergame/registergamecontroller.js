var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterGameController', //['$scope', '$http','GameSettings',
    function ($scope, GameSettings, Players) {
        $scope.game = {gameType: "", mapStyle: "", location: "", size: "", resources: "", gameSpeed: "", victory: "", players: []};
        $scope.gametypes = GameSettings.query({settingName: "gametypes"});
        $scope.mapstyles = GameSettings.query({settingName: "mapstyles"});
        $scope.locations = GameSettings.query({settingName: "location"});
        $scope.sizes = GameSettings.query({settingName: "sizes"});
        $scope.resourcesList = GameSettings.query({settingName: "resourceslist"});
        $scope.gameSpeeds = GameSettings.query({settingName: "gamespeeds"});
        $scope.victoryList = GameSettings.query({settingName: "victorylist"});
        $scope.civilizations = GameSettings.query({settingName: "civilizations"});
        $scope.allPlayers = Players.query();

        for (i = 0; i < 8; i++) {
            $scope.game.players.push({'nickname': "", 'civilization': "", 'team': 0, 'iswinner': false});
        }
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