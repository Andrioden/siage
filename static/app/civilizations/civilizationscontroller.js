var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('CivilizationsController',
    function ($rootScope, $scope, Civilization, $location) {

        $scope.loading_civilizations = true;
        Civilization.query(
            function (data) {
                $scope.civilizations = data;
                $scope.setBestPlayersForCivs();
                $scope.loading_civilizations = false;
                $scope.error = "";
            }
            ,function(error){
                $scope.loading_civilizations = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });

        $scope.navigate = function (route) {
            $location.path(route);
        };


        $scope.setBestPlayersForCivs = function () {
            for (i = 0; i < $scope.civilizations.length; i++) {
                $scope.civilizations[i].stats.player_fit.sort(comparePointsForPlayers);
                $scope.civilizations[i].stats.best_players = $scope.civilizations[i].stats.player_fit.slice(0,3);
            };
        };

        function comparePointsForPlayers(a, b) {
            if (a.points < b.points)
                return -1;
            if (a.points > b.points)
                return 1;
            return 0;
        }
    });