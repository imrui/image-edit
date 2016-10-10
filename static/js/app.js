var imageApp = angular.module('imageApp', [
  'ngRoute',
  'ngCookies',
  'imageControllers',
  'imageServices'
]);

imageApp.controller('MainCtrl', ['$scope', '$cookies', '$filter', '$http', '$log',
  function ($scope, $cookies, $filter, $http, $log) {

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
