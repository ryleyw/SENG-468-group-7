import TotalsDisplay from './totalsDisplay'
import DisplayContainer from './infoDisplay/displayContainer'
import '../css/main.css'

function MainContainer(props) {
    return(
        <div className="main">
            {props.user==null ?
                (<div>
                    Please log in to view your account info
                </div>)
                :
                (<div>
                    <div className="welcome">Welcome {props.user}!</div>
                    <TotalsDisplay user={props.user} info={props.info} setInfo={props.setInfo}/>
                    <DisplayContainer user={props.user} info={props.info}/>
                </div>)
            } 
        </div>
    )
}

export default MainContainer