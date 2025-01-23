var tables_schema = {};
var tables_data = {};
var cur_Table = null;
var loading_modal = null;

async function show_dialog(id) {
    let modal = document.querySelector(`#${id}`);
    if (modal) {
        modal.showModal();
    }
    else
    {
        loading_modal.showModal();
        let res = await fetch(`/m/${id}`);
        let [html, status] = res.ok ? [await res.text(),res.status] : [null, res.status];
        if (!html) {
            alert('response status ' + status);
            loading_modal.close();
            return;
        }
        let doc = new DOMParser().parseFromString(html, 'text/html').body;
        modal = document.body.appendChild(doc.children[0]);
        loading_modal.close();
    }
    modal.showModal();
    if(id == 'new_rows')
    {
        
    }
}

async function create_table() {
    //{table_name: [{colname: str, type: str, nullable: bool, pk: bool, unique: bool}]}
    loading_modal.showModal();
    let t_tbl_nm = document.querySelector('#new_table .table_name').innerText.trim();
    let t_tbl = { [t_tbl_nm]: [] };
    let types = {
        String: 'str',
        Integer: 'int',
        Float: 'float',
        Boolean: 'bool',
        DateTime: 'datetime',
        Date: 'date',
        Time: 'time'
    }
    document.querySelectorAll('#new_table tbody tr').forEach(tr => {
        let col = [];
        let colnm = ['colname', 'type', 'pk', 'nullable', 'unique'];
        tr.querySelectorAll('td').forEach(td => {
            if (td.firstElementChild.type == 'checkbox') {
                col.push(td.firstElementChild.checked);
            }
            else
                col.push(td.firstElementChild.value);
        })
        let colObj = {};
        for (let i = 0; i < col.length; i++)
            colObj[colnm[i]] = i == 1 ? types[col[i]] : col[i];
        console.log(colObj);
        t_tbl[t_tbl_nm].push(colObj);
    })

    let res = await fetch(`/api/table/${JSON.stringify(t_tbl)}`,{method:'POST'});
    loading_modal.close();
    if (res.ok) {
        document.querySelector('#new_table').close();
    }   
    else
        alert('failed '+res.status);
    return;
}


function tpop_column()
{
    if(document.querySelector('#new_table tbody').childElementCount == 1)
        return;
    document.querySelector('#new_table tbody').lastElementChild.remove();
} 

async function select_table(tabl_name) {
    cur_Table = tables_schema[tabl_name];
    set_colnames();
    data = await fetch('/api/table/' + tabl_name.trim()).then(res => res.json());
}

function clear_coln() {
    col_n = document.querySelector('#col_n');
    col_d = document.querySelector('tbody');

    while (col_n.firstChild) {
        col_n.removeChild(col_n.firstChild)
    }
    while (col_d.firstChild) {
        col_d.removeChild(col_d.firstChild)
    }
}

function set_colnames(tabl_name=cur_Table.tabl_name, selector='#col_n') {
    tables_schema[tabl_name].cols.forEach(col => {
        let th = document.createElement('th');
        th.innerText = col.colname;
        document.querySelector(selector).appendChild(th);
    });
}

$(async () => {
     loading_modal = document.querySelector('#loading');
    tables_schema = await fetch('/api/tables').then(res => res.json());
    console.log(tables_schema['test']);
    let first = true;

    for (k in tables_schema) {
        table = tables_schema[k]
        if (first) {
            cur_Table = table;
            first = false;
        }
        let elem = document.querySelector('#tab_template').cloneNode(deep = true);
        elem.id = '';
        elem.classList.toggle('hidden');
        elem.classList.toggle('table');
        elem.querySelector('#table_name').innerText = table.tabl_name;
        elem.dataset.tabl_name = table.tabl_name;
        elem = document.querySelector('.sidebar').appendChild(elem);

        elem.onclick = () => {
            clear_coln();

            elm = elem.firstElementChild;
            if (elm.classList.contains('selected')) {
                elm.classList.toggle('selected');
                return;
            }
            document.querySelectorAll('.table-item').forEach(el => el.classList.remove('selected'));
            elm.classList.toggle('selected');

            select_table(elem.dataset.tabl_name);
        }

    }
    if (cur_Table)
        set_colnames(cur_Table.tabl_name);



})