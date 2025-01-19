1. Installing Terraform in Codespaces
Option 1: Using the Codespace Terminal
You can directly install Terraform in the Codespaces terminal by following these steps:

Open the terminal in your Codespace.
Add the HashiCorp repository:
bash
```
sudo apt-get update
sudo apt-get install -y gnupg software-properties-common
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update
```

3. Install Terraform:
bash
```
sudo apt-get install -y terraform

```

4. Verify installation
```
terraform version
```

Running tf commands

```terraform init #Initialise
terraform fmt #format files
terraform plan # run conditions
terraform apply # apply conditions
```


