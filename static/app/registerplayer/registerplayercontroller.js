var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterPlayerController',
    function ($scope, Player, $timeout) {
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
                    $scope.success = value.response;
                    $timeout(function(){
                        $scope.success = "";
                    }, 5000);
                },
                //error
                function (error) {
                    console.log(error);
                    $scope.error = error.data;
                }
            )
        }

        $scope.hideError = function(){
            $scope.error = "";
        }
    });
