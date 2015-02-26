var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('RegisterPlayerController',
    function ($scope, Player) {
        $scope.newplayer = new Player();
        $scope.newplayer.nick = "";

        Player.query(
            function (data) {
                $scope.players = data;
            }
            , function (error) {
                $scope.playerListError = "Unable to load players list!";
            });

        $scope.submitPlayer = function () {
            Player.save($scope.newplayer).$promise.then(
                //success
                function( value ){ alert('Saved player') },
                //error
                function( error ){ alert('Failed to save player. Error: ' + error)}
            )
        }
    });
