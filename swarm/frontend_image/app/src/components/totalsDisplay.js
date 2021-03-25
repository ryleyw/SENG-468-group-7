import React, {useState} from 'react'
import axios from 'axios'

function TotalsDisplay(props) {

    const [showModal, setShowModal] = useState(false)
    const [moneyAdd, setMoneyAdd] = useState(0)

    function handleChange(e) {
        console.log(e.target.value.toString())
        setMoneyAdd(e.target.value)
    }

    function addMoney(e) {
        e.preventDefault()
        console.log(moneyAdd)
        const data = {
            'command': 'ADD',
            'userid': props.user,
            'amount': moneyAdd.toString()
        }
        axios.post('http://localhost:81/', data).
            then((response) => {
                props.setInfo(response.data.result)
            }, (error) => {
                alert(error)
            })
        setMoneyAdd(0)
    }

    const modal = (
        <div className="modal">
            <button onClick={() => setShowModal(false)}>close</button>
            <div>
            Enter amount of money to add:
                <form onSubmit={addMoney}>
                    <input type="number" onChange={handleChange} value={moneyAdd}></input>
                    <input type="submit" className="addButton" value="add cash"></input>
                </form>
            </div>
        </div>
    );

    return (
        <div className="totals">
        {props.info !=null &&
            (<div>
                <div className="totalsAmount">
                {props.info.cash} $
                </div>
                <div className="addCash">
                    <button onClick={() => setShowModal(true)}>Add cash</button>
                </div>
            </div>)
        }
        {showModal &&
            (<div>
              {modal}
            </div>)
        }
            
        </div>
    )
}

export default TotalsDisplay

