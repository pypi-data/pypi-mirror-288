(self.webpackChunkmrx_link_git=self.webpackChunkmrx_link_git||[]).push([[201],{81201:function(e){var r;e.exports=(r=function(){this.listeners={},this.registerListener=function(r,n,t){var i=r.constructor.name;t=this.validateNumber(t||"any"),"Array"!==i&&(r=[r]),r.forEach((function(r){if("String"!==r.constructor.name)throw new Error("Only `String` and array of `String` are accepted for the event names!");e.listeners[r]=e.listeners[r]||[],e.listeners[r].push({callback:n,number:t})}))},this.validateNumber=function(e){var r=e.constructor.name;if("Number"===r)return e;if("String"===r&&"any"===e.toLowerCase())return"any";throw new Error("Only `Number` and `any` are accepted in the number of possible executions!")},this.toBeRemoved=function(e){var r=e.number;return e.execution=e.execution||0,e.execution++,!("any"===r||e.execution<r)};var e=this;return{on:function(r,n){e.registerListener.bind(e)(r,n,"any")},once:function(r,n){e.registerListener.bind(e)(r,n,1)},exactly:function(r,n,t){e.registerListener.bind(e)(n,t,r)},die:function(r){delete e.listeners[r]},off:function(e){this.die(e)},detach:function(r,n){if(void 0===n)return e.listeners[r]=[],!0;for(var t in e.listeners[r])if(e.listeners[r].hasOwnProperty(t)&&e.listeners[r][t].callback===n)return e.listeners[r].splice(t,1),this.detach(r,n);return!0},detachAll:function(){for(var r in e.listeners)e.listeners.hasOwnProperty(r)&&this.detach(r)},emit:function(r,n){var t=[];for(var i in e.listeners)if(e.listeners.hasOwnProperty(i)&&(i===r&&Array.prototype.push.apply(t,e.listeners[i]),i.indexOf("*")>=0)){var s=i.replace(/\*\*/,"([^.]+.?)+");s=s.replace(/\*/g,"[^.]+");var a=r.match(s);a&&r===a[0]&&Array.prototype.push.apply(t,e.listeners[i])}var o=arguments;n=n||this,t.forEach((function(t,i){var s=t.callback;t.number,n&&(s=s.bind(n));var a=[];Object.keys(o).map((function(e){e>1&&a.push(o[e])})),e.toBeRemoved(t)&&e.listeners[r].splice(i,1),s.apply(null,a)}))}}},r),e.exports.default=e.exports}}]);