var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterPlayerController',
    function ($scope, Player) {
        $scope.newplayer = new Player();

        Player.query(
            function (data) {
                $scope.players = data;
            }
            , function (error) {
                $scope.error = "Unable to load players list!";
            });

        $scope.submitPlayer = function () {
            Player.save($scope.newplayer).$promise.then(
                //success
                function (value) {
                    $scope.players.push($scope.newplayer);
                    $scope.newplayer = new Player();
                    $scope.error = "";
                },
                //error
                function (error) {
                    $scope.error = 'Failed to save player.  ' + error.statusText;
                }
            )
        }
    });
