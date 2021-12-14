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
                     <draggable v-model="lift.request" group="requests" @start="drag=true" @end="onDragEnd" class="list-group">
                       <div v-for="request in lift.request" :key="request.id" class="list-group-item">
                       {{ request.skydiver_last_name }} {{ request.skydiver_first_name }}, {{ request.height }} м
                         <div> {{ request.discipline_name}}, {{ request.creationStamp }}</div>
                       </div>
                     </draggable>
                     <div v-if="lift.request.length==0">Заявки отсутствуют.</div>
                   </b-card-body>
                 </b-collapse>
               </b-card>`,
    methods: {
        onDragEnd(event){
            let fromRequestElement = event.from.__vue__.context.element
            this.$root.$emit('bind-request', false, this['lift'].id, fromRequestElement.id, fromRequestElement.discipline_id);
        }
    }
});

Vue.component('lift-request-list-item', {
    props: ['request', 'lift_id'],
    template: `<b-list-group-item :id="'req_' + request.id">
                    <div>{{ request.discipline_name }}, {{ request.skydiver_name }}</div>
                    <div> {{ request.height }} м</div>
                    <button class="btn btn-primary" v-on:click="UnbindRequestFromLift">&gt;</button>
                </b-list-group-item>`,
    methods: {
        UnbindRequestFromLift: function () {
            this.$root.$emit('bind-request', false, this['lift_id'], this['request'].id, this['request'].discipline_id);
        }
    }
});

Vue.component('disc-request-list-item', {
    model: {
        event: 'bind-request'
    },
    props: ['request'],
    template: `<b-list-group-item :key="request.id" :id="'req_' + request.id">
                 <button class="btn btn-primary" v-on:click="BindRequestToLift">&lt;</button>
                 <div>{{ request.skydiver_name }}, {{ request.height }} м</div>
                 <div> {{ request.creationStamp }}</div>
               </b-list-group-item>`,
    methods: {
        BindRequestToLift: function () {
            this.$root.$emit('bind-request', true, -1, this['request'].id, this['request'].discipline_id)
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
            let response = await fetch('/api/discipline/')
            this.disciplinesList = await response.json()
        },
        async getLifts(){
            let response = await fetch('/api/lift/?pDay=' + this.currentDay)
            this.liftsList = await response.json()
        },
        getCookie(name) {
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
        },
        async BindRequestToLift(pIsBind, liftId, requestId, discipline_id){
            let selectedLifts = this.liftsList.filter(lift => {
                return lift.visible === true
            })
            if (selectedLifts.length == 0){
                alert('Не выбран подъем для включения заявки.');
                return;
            }
            let selectedLift = selectedLifts[0]
            liftId = selectedLift.id
            
            const csrftoken = this.getCookie('csrftoken');
            let response = await fetch('/bind_request_to_lift/', {
                                            method: 'POST',
                                            headers: {
                                                'X-CSRFToken': csrftoken,
                                                'Content-Type': 'application/json;charset=utf-8'
                                            },
                                            body: JSON.stringify({request_id: requestId,
                                                                    lift_id: liftId,
                                                                    is_bind: pIsBind })
                                            });

            let resp = await response.json()
            if (resp.status != 'OK')
                alert('При выполнении операции произошла ошибка.')
            else
                this.getRequests()
        },
        onDragEnd(event){
            let fromRequestElement = event.from.__vue__.context.element
            this.BindRequestToLift(true, -1, fromRequestElement.id, fromRequestElement.discipline_id)
        }
    },
    created(){
        this.$root.$on('bind-request', (isBind, liftId, requestId, disciplineId) => {
            this.BindRequestToLift(isBind, liftId, requestId, disciplineId)
        })

        let today = new Date();
        let mm = today.getMonth() + 1;
        let dd = today.getDate();

        this.currentDay = today.getFullYear() + '-' + (mm>9 ? '' : '0') + mm + '-' + (dd>9 ? '' : '0') + dd;

        this.getLifts()
        this.getRequests()
    }
  })