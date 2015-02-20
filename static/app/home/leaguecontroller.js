var siAgeApp = angular.module('SiAgeApp');

siAgeApp.controller('LeagueController', ['$scope', '$http',
function($scope, $http) {
	$scope.players = [];
	init($scope, $http);

	/*function init() {
		$scope.players = [{
			name : 'Shrubber',
			rating : 1520,
			winpct : 66,
			favciv : 'Britons'
		}, {
			name : 'Android',
			rating : 1543,
			winpct : 73,
			favciv : 'French'
		}, {
			name : 'FreddyFearless',
			rating : 1523,
			winpct : 69,
			favciv : "Huns"
		}];*/

		function init($scope, $http) {
			$http.get('/api/players').success(function(data) {
				$scope.players = angular.fromJson(data);
			});
	};

	$scope.addPlayer = function() {

		if ($scope.newplayer != null && $scope.newplayer != '') {
			$scope.players.push({
				name : $scope.newplayer,
				rating : 1500
			});
		};

		// Clear input fields after push
		$scope.newplayer = "";
	};
}]); 