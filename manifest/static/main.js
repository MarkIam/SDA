function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function BindRequestToLift(elem, pIsBind)
{
    const csrftoken = getCookie('csrftoken');
    
    let selectedLift = document.querySelectorAll('#liftsGroup .accordion-item button[aria-expanded="true"]')
    if (selectedLift.length == 0){
        alert('Не выбран подъем для включения заявки.');
        return;
    }
    let liftId = document.querySelectorAll('#liftsGroup .accordion-item button[aria-expanded="true"]')[0].parentElement.parentElement.id.substr(5)
    
    let requestId = elem.parentElement.id.substr(4)

    let response = await fetch('http://127.0.0.1:8000/bind_request_to_lift/', {
                                    method: 'POST',
                                    headers: {
                                        'X-CSRFToken': csrftoken,
                                        'Content-Type': 'application/json;charset=utf-8'
                                    },
                                        body: JSON.stringify({request_id: requestId,
                                                              lift_id: liftId,
                                                              is_bind: pIsBind })
                                    });

    let status = await response.json()
    if (status.status=='OK'){
        app.getLifts();
        app.getRequests();
    }
    else
        alert('При выполнении операции произошла ошибка.')
}

Vue.component('lift-item', {
    props: ['lift', 'index'],
    template: `<b-card no-body class="mb-1">
                 <b-card-header header-tag="header" class="p-1" role="tab">
                   <b-button block v-b-toggle="'accordion-' + lift.id" variant="info">
                     {{ lift.ord_number }}. {{ lift.plane_reg_number }}
                   </b-button>
                 </b-card-header>
                 <b-collapse :id="'accordion-' + lift.id" accordion="lifts-accordion" v-model:visible="lift.visible" role="tabpanel">
                   <b-card-body>
                     <b-list-group :id="'list-group-' + lift.id">
                       <lift-request-list-item
                            v-for="request in lift.requests"
                            v-bind:key="request.id"
                            v-bind:request="request"
                            v-bind:lift_id="lift.id">
                       </lift-request-list-item>
                     </b-list-group>
                     <div v-if="lift.requests.length==0">Заявки отсутствуют.</div>
                   </b-card-body>
                 </b-collapse>
               </b-card>`
});

Vue.component('lift-request-list-item', {
    props: ['request', 'lift_id'],
    template: `<b-list-group-item :id="'req_' + request.id">
                    <div>{{ request.name }}</div>
                    <button class="btn btn-primary" v-on:click="RemoveRequestFromLift">&gt;</button>
                </b-list-group-item>`,
    methods: {
        RemoveRequestFromLift: function () {
            alert(this['lift_id'] + ',' + this['request'].id);
        }
    }
});

Vue.component('disc-request-list-item', {
    props: ['request'],
    template: `<b-list-group-item :key="request.id" :id="'req_' + request.id">
                 <button class="btn btn-primary" v-on:click="BindRequestToLift">&lt;</button>
                 <div>{{ request.skydiver_name }}, {{ request.height }} м</div>
                 <div> {{ request.creationStamp }}</div>
               </b-list-group-item>`,
    methods: {
        BindRequestToLift: function () {
            alert(this['request'].id);
        }
    }
});

var app = new Vue({
    el: '#vueApp',
    data: {
        currentDay: '-',
        disciplinesList:[],
        liftsList:[]
    },
    methods:{
        async getRequests(){
            let response = await fetch('/manifest/request/json')
            this.disciplinesList = await response.json()
        },
        async getLifts(){
            let response = await fetch('/manifest/lift/json?pDay=' + this.currentDay)
            this.liftsList = await response.json()
        }
    },
    created(){
        let today = new Date();
        let mm = today.getMonth() + 1;
        let dd = today.getDate();

        this.currentDay = today.getFullYear() + '-' + (mm>9 ? '' : '0') + mm + '-' + (dd>9 ? '' : '0') + dd;

        this.getLifts()
        this.getRequests()
    }
  })