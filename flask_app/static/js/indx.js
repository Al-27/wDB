var tables_schema = {};
var tables_data = {};
var cur_Table = null;



async function select_table(tab_name)
{
    cur_Table = tables_schema[tab_name];
    data = await fetch('/api/table/'+tab_name.trim()).then(res=>res.json());
    set_coln(tab_name);
}

function clear_coln()
{
    col_n = document.querySelector('#col_n');
    col_d = document.querySelector('tbody');

    while (col_n.firstChild) {
        col_n.removeChild(col_n.firstChild)
    }
    while (col_d.firstChild) {
        col_d.removeChild(col_d.firstChild)
    }
}

function set_coln(tab_name)
{ 
    tables_schema[tab_name].cols.forEach( col => {
        let th = document.createElement('th');
        th.innerText = col.colname;
        document.querySelector('#col_n').appendChild(th);
    });
}

$(async ()=> {
    cur_Table
    tables_schema = await fetch('/api/tables').then(res=>res.json());
    console.log(tables_schema['test']);
    let first = true;

    for(k in tables_schema)
    {
        table = tables_schema[k]
        if (first) {
            cur_Table = table;
            first = false;
        }
        let elem = document.querySelector('#tab_template').cloneNode(deep=true);
        elem.id = '';
        elem.classList.toggle('hidden');
        elem.classList.toggle('table');
        elem.querySelector('#table_name').innerText = table.tab_name;
        elem.dataset.tab_name = table.tab_name;
        elem = document.querySelector('.sidebar').appendChild(elem);

        elem.onclick = ()=>{
            clear_coln();

            elm = elem.firstElementChild;
            if( elm.classList.contains('selected') )
            {
                elm.classList.toggle('selected');
                return;
            }
            document.querySelectorAll('.table-item').forEach(el=>el.classList.remove('selected'));
            elm.classList.toggle('selected');
            
            select_table(elem.dataset.tab_name);
        } 
        
    }
    
    set_coln(cur_Table.tab_name);
})