var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterPlayerController',
    function ($rootScope, $scope, Player, $timeout) {
        $scope.newplayer = new Player();

        $scope.loading_players = true;
        Player.query(
            function (data) {
                $scope.loading_players = false;
                $scope.players = data;
                $scope.error = "";
            }
            , function (error) {
                $scope.loading_players = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            });

        $scope.submitPlayer = function () {
            Player.save($scope.newplayer).$promise.then(
                //success
                function(value) {
                    $scope.players.push(value.player);
                    $scope.newplayer = new Player();
                    $scope.error = "";
                    $scope.success = value.response;
                    $timeout(function() {
                        $scope.success = "";
                    }, 5000);
                },
                //error
                function(error) {
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                }
            );
        };

        $scope.hideError = function(){
            $scope.error = "";
        };
    });
