var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('GameController',
    function ($rootScope, $scope, Game, $routeParams, FilesAction, FileUploader) {

        $scope.file_uploader = new FileUploader({
            onAfterAddingFile: setFileUploadItemUrl,
            onCompleteItem: function(item, response, status, headers) {
                $scope.file_uploader.removeFromQueue(item);
            },
            onSuccessItem: function(item, response, status, headers) {
                $scope.game.files.push(response.file);
            },
            onErrorItem: function(item, response, status, headers) {
                $scope.error += "File not added. " + $rootScope.getFriendlyErrorText(response);
            }
        });

        $scope.loading_game = true;

        Game.get({ game_id: $routeParams.gameId, data_detail: 'full' },
            function (data) {
                $scope.game = data;
                $scope.file_uploader.formData = [{game_id: $scope.game.id}];
                $scope.error = "";
                $scope.loading_game = false;
            },
            function (error) {
                $scope.loading_game = false;
                $scope.error = $rootScope.getFriendlyErrorText(error);
            }
        );

        // PUBLIC METHODS

        $scope.deleting_game_file = false;

        $scope.deleteGameFile = function(game_file_id) {
            $scope.deleting_game_file = true;
            FilesAction.deleteGameFile({ game_file_id: game_file_id}).$promise.then(
                //success
                function (data) {
                    for(var i=0; i<$scope.game.files.length; i++) {
                        if ($scope.game.files[i].id == game_file_id) $scope.game.files.splice(i,1);
                    }
                    $scope.error = "";
                    $scope.deleting_game_file = false;
                },
                //error
                function (error) {
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                    $scope.deleting_game_file = false;
                }
            );
        }


        // PRIVATE METHODS

        function setFileUploadItemUrl(item) {
            $scope.loading_upload_url = true;
            FilesAction.getUploadGameFileUrl().$promise.then(
                //success
                function (data) {
                    item.url = data.upload_url
                    $scope.loading_upload_url = false;
                },
                //error
                function (error) {
                    $scope.error = $rootScope.getFriendlyErrorText(error);
                    $scope.loading_upload_url = false;
                }
            );
        }

    }
);