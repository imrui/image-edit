var imageServices = angular.module('imageServices', ['ngResource']);

imageServices.factory('IconMerge', ['$resource',
  function ($resource) {
    return $resource('/icon/merge');
  }]);

imageServices.factory('Watermark', ['$resource',
  function ($resource) {
    return $resource('/watermark');
  }]);
