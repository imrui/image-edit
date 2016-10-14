var imageApp = angular.module('imageApp', [
  'ngRoute',
  'ngCookies',
  'imageControllers',
  'imageServices'
]);

imageApp.controller('MainCtrl', ['$scope', '$cookies', '$filter', '$http', '$log',
  function ($scope, $cookies, $filter, $http, $log) {
    $http.get('/app/icon/set').success(function(data) {
      $scope.downloadHost = data.downloadHost;
      $scope.appIconSet = data.appIconSet;
      $log.debug($scope.downloadHost);
      $log.debug($scope.appIconSet);
      $scope.$broadcast('on_finish_app_icon_set');
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
    };
    $scope.setImgCookies = function (key, value) {
      $cookies.put(key, value);
    };
    $scope.getImgCookies = function (key) {
      return $cookies.get(key);
    };
    $scope.removeImgCookies = function (key) {
      return $cookies.remove(key);
    };
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
