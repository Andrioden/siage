var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterPlayerController',
    function ($scope, Player, $timeout) {
        $scope.newplayer = new Player();

        $scope.loading_players = true;
        Player.query(
            function (data) {
                $scope.loading_players = false;
                $scope.players = data;
            }
            , function (error) {
                $scope.loading_players = false;
                $scope.error = "Unable to load players list!";
            });

        $scope.submitPlayer = function () {
            Player.save($scope.newplayer).$promise.then(
                //success
                function(value) {
                    $scope.players.push($scope.newplayer);
                    $scope.newplayer = new Player();
                    $scope.error = "";
                    $scope.success = value.response;
                    $timeout(function() {
                        $scope.success = "";
                    }, 5000);
                },
                //error
                function(error) {
                    if (error.data.error_code == "VALIDATION_ERROR_NOT_LOGGED_INN") {
                        $scope.error = "You need to login to use this function.";
                    }
                    else if (error.data.error_code == "VALIDATION_ERROR_NOT_AUTHENTICATED") {
                        $scope.error = "You need to claim an existing player before you can register other players.";
                    }
                    else {
                        $scope.error = error.data.error_message;
                    };
                }
            );
        };

        $scope.hideError = function(){
            $scope.error = "";
        };
    });
