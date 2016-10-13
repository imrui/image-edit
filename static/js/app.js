var imageApp = angular.module('imageApp', [
  'ngRoute',
  'ngCookies',
  'imageControllers',
  'imageServices'
]);

imageApp.controller('MainCtrl', ['$scope', '$cookies', '$filter', '$http', '$log',
  function ($scope, $cookies, $filter, $http, $log) {
    $http.get('/app/icon/set').success(function(data) {
      $scope.appIconSet = data;
      $log.debug($scope.appIconSet);
    });
    $scope.afterUpload = function (data) {
      $log.debug(data);
      var category = data.category;
      var filePath = data.directory + '/' + data.filename;
      $cookies.put(category, filePath);
      $scope[category] = filePath;
      $log.debug('after ' + $scope[category]);
    };
    $scope.refreshImage = function (category) {
      var filePath = $cookies.get(category);
      if (filePath) {
        $log.debug(category, filePath);
        $scope[category] = filePath;
      }
    }
  }]);

imageApp.config(['$routeProvider', '$httpProvider', '$logProvider',
  function ($routeProvider, $httpProvider, $logProvider) {
    $logProvider.debugEnabled(true);
    $routeProvider.
      when('/icon', {
        templateUrl: 'static/partials/icon.html',
        controller: 'IconCtrl'
      }).
      when('/watermark', {
        templateUrl: 'static/partials/watermark.html',
        controller: 'WatermarkCtrl'
      }).
      otherwise({
        redirectTo: '/icon'
      });
  }]);
