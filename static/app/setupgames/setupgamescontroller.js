var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('SetupGamesController',
    function ($scope, Player, SetupGame, $routeParams) {
        $scope.all_joining = false;
        $scope.loading_players = true;
        Player.query(
            function (data) {
                for (var i = 0; i < data.length; i++) {
                    data[i].win_percent = Math.round(data[i].wins * 100 / data[i].played);
                };
                $scope.players = data;
                $scope.loading_players = false;
            }
            , function (error) {
                $scope.loading_players = false;
                $scope.error = "Unable to load league list!";
            });

        $scope.setupGame = function () {
            $scope.players_joining = [];
            for (var i = 0; i < $scope.players.length; i++) {
                if ($scope.players[i].joining) {
                    $scope.players_joining.push($scope.players[i]);
                };
            }

            //TODO: Sende med parameter som inneholder spillere
            SetupGame.generate(
                function (data) {
                    $scope.games = data.games;
                    //{"games": [{"rating_dif": 899, "teams": [[{"nick": "Shrubber", "id": 5144752345317376, "rating": 1000}, {"nick": "Fredrik", "id": 4863277368606720, "rating": 950}], [{"nick": "Lise", "id": 5707702298738688, "rating": 1051}]]}], "total_rating_dif": 899}
                }
            , function (error) {
                $scope.error = "Unable to setup game!";
            });

            
        };
    }
);