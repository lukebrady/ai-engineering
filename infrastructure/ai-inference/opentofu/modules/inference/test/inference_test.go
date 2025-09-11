package test

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/openai/openai-go"
	"github.com/stretchr/testify/require"
)

const (
	maxRetries    = 60
	sleepDuration = 30 * time.Second
)

// testModel is a helper function to test the deployed model
func testModel(t *testing.T, publicIP, modelName string) {
	t.Helper()

	config := openai.DefaultConfig("whatever")
	config.BaseURL = fmt.Sprintf("http://%s:8000/v1", publicIP)

	client := openai.NewClientWithConfig(config)

	// Wait for the model to be ready
	require.Eventually(t, func() bool {
		_, err := client.ListModels(context.Background())
		return err == nil
	}, maxRetries*sleepDuration, sleepDuration, "model was not ready in time")

	// Send a request to the model
	resp, err := client.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model: modelName,
			Messages: []openai.ChatCompletionMessage{
				{
					Role:    openai.ChatMessageRoleUser,
					Content: "Hello!",
				},
			},
		},
	)
	require.NoError(t, err, "failed to create chat completion")
	require.NotEmpty(t, resp.Choices, "got an empty response")
	require.NotEmpty(t, resp.Choices[0].Message.Content, "got an empty message")
}

// TestQwen3_0_6B tests the qwen3-0.6b example
func TestQwen3_0_6B(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../examples/qwen3-0.6b",
		Vars: map[string]interface{}{
			"allowed_ip_addresses": getMyPublicIP(t),
			"hugging_face_token":   os.Getenv("HUGGING_FACE_TOKEN"),
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	publicIP := terraform.Output(t, terraformOptions, "public_ip")
	require.NotEmpty(t, publicIP, "public_ip output was empty")

	testModel(t, publicIP, "Qwen/Qwen3-0.6B")
}

// TestGemma3_27B tests the gemma-3-27b-it example
func TestGemma3_27B(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../examples/gemma-3-27b-it",
		Vars: map[string]interface{}{
			"allowed_ip_addresses": getMyPublicIP(t),
			"hugging_face_token":   os.Getenv("HUGGING_FACE_TOKEN"),
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	publicIP := terraform.Output(t, terraformOptions, "public_ip")
	require.NotEmpty(t, publicIP, "public_ip output was empty")

	testModel(t, publicIP, "google/gemma-3-27b-it")
}

// getMyPublicIP returns the public IP of the machine running the test
func getMyPublicIP(t *testing.T) []string {
	t.Helper()

	resp, err := http.Get("https://api.ipify.org")
	require.NoError(t, err, "failed to get public IP")
	defer resp.Body.Close()

	ip, err := io.ReadAll(resp.Body)
	require.NoError(t, err, "failed to read public IP response")

	return []string{fmt.Sprintf("%s/32", strings.TrimSpace(string(ip)))}
}
