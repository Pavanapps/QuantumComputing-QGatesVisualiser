from flask import Flask, render_template, request
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_bloch_multivector, plot_histogram
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)

STATIC_FOLDER = "static"

if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)


def save_plot(fig):
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(STATIC_FOLDER, filename)

    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)

    return filename


@app.route("/", methods=["GET", "POST"])
def index():

    result = None

    # default values
    gate = "H"
    angle = ""

    if request.method == "POST":

        gate = request.form.get("gate")
        angle = request.form.get("angle")

        qc = QuantumCircuit(1)

        # Apply Gates
        if gate == "X":
            qc.x(0)

        elif gate == "Y":
            qc.y(0)

        elif gate == "Z":
            qc.z(0)

        elif gate == "H":
            qc.h(0)

        elif gate == "RX":
            qc.rx(float(angle), 0)

        elif gate == "RY":
            qc.ry(float(angle), 0)

        elif gate == "RZ":
            qc.rz(float(angle), 0)

        # Statevector
        state = Statevector.from_instruction(qc)

        # Probabilities
        probs = state.probabilities_dict()

        # Explanation
        explanation = ""

        if gate == "H":
            explanation = (
                "The Hadamard gate creates superposition, "
                "giving nearly equal probabilities of measuring 0 and 1."
            )

        elif gate == "X":
            explanation = (
                "The Pauli-X gate flips the qubit state "
                "from |0⟩ to |1⟩."
            )

        elif gate == "Y":
            explanation = (
                "The Pauli-Y gate rotates the qubit "
                "around the Y-axis while introducing phase change."
            )

        elif gate == "Z":
            explanation = (
                "The Pauli-Z gate changes the qubit phase "
                "without affecting measurement probabilities."
            )

        elif gate == "RX":
            explanation = (
                f"The RX gate rotates the qubit around the X-axis "
                f"by {angle} radians."
            )

        elif gate == "RY":
            explanation = (
                f"The RY gate rotates the qubit around the Y-axis "
                f"by {angle} radians."
            )

        elif gate == "RZ":
            explanation = (
                f"The RZ gate rotates the qubit around the Z-axis "
                f"by {angle} radians."
            )

        # Bloch Sphere
        bloch_fig = plot_bloch_multivector(state)
        bloch_img = save_plot(bloch_fig)

        # Histogram
        hist_fig = plot_histogram(probs)
        hist_img = save_plot(hist_fig)

        # Circuit Diagram
        circuit_fig = qc.draw(output="mpl")
        circuit_img = save_plot(circuit_fig)

        result = {
            "statevector": str(state),
            "bloch_img": bloch_img,
            "hist_img": hist_img,
            "circuit_img": circuit_img,
            "probabilities": probs,
            "explanation": explanation
        }

    return render_template(
        "index.html",
        result=result,
        selected_gate=gate,
        selected_angle=angle
    )


if __name__ == "__main__":
    app.run(debug=True)