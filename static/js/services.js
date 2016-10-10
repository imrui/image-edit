var imageServices = angular.module('imageServices', ['ngResource']);

imageServices.factory('Icon', ['$resource',
  function ($resource) {
    return $resource('/icon');
  }]);
